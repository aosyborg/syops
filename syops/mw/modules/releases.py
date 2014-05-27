import os
import shutil
import logging
import json
import tempfile
import subprocess
import boto.sqs
from httplib2 import Http
from urllib import urlencode
from boto.sqs.message import Message

from syops.mw.modules import Abstract
from syops.lib.application import Application
from syops.lib.models.user import User
from syops.lib.models.team import Team
from syops.lib.models.app import App
from syops.lib.models.release import Release
from syops.lib.models.github import Github

STATUS_PENDING_QA = 1
STATUS_FAILED = 2
STATUS_IN_QA = 3
STATUS_PENDING_PROD = 4
STATUS_IN_PROD = 5

class Releases(Abstract):

    def init(self):
        from syops.lib.application import Application
        self.sqs = boto.sqs.connect_to_region(
            'us-east-1',
            aws_access_key_id=Application.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Application.AWS_SECRET_ACCESS_KEY)
        self.queue = self.sqs.get_queue('syops-releases')

    def loop(self):
        messages = self.queue.get_messages(1)
        for message in messages:
            payload = json.loads(message.get_body())
            self.queue.delete_message(message)
            logging.info('Release info recieved: %s' % payload)

            # Grab release id
            release_id = payload.get('release_id')
            if not release_id:
                logging.warning('No release id found!')

            # Ensure there is work to be done
            release = Release(release_id)
            if release.release_status_id != STATUS_PENDING_QA and \
               release.release_status_id != STATUS_PENDING_PROD:
                logging.warning('Nothing to do')
                continue

            # Build package and place in QA
            if release.release_status_id == STATUS_PENDING_QA:
                self.build(release)
                continue;

            # Copy package to prod
            if release.release_status_id == STATUS_PENDING_PROD:
                self.copy_to_prod(release)

    def build(self, release):
        app = App(release.app_id)
        team = Team(app.team_id)
        user = User(team.user_id)

        # Ensure build instructions present
        logging.info('Building %s v%s...' % (app.name, release.version))
        if not app.build_instructions:
            logging.warning('No build instructions found!')
            return

        # Make clean dir to build in
        build_dir = '/tmp/syops/%s_%s' % (app.name, release.version)
        cmd = 'mkdir -p /tmp/syops && git clone https://%s@%s -b %s %s' % (
            user.access_token,
            app.clone_url.replace('https://', ''),
            release.tagged_branch,
            build_dir
        )
        child = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
        output, errors = child.communicate()
        return_code = child.returncode

        # Replace magic variables
        build_inst = app.build_instructions.replace('__DIR__', build_dir)
        build_inst = build_inst.replace('__APPNAME__', app.name)
        build_inst = build_inst.replace('__VERSION__', release.version)
        build_inst = build_inst.replace('\r', '')

        # Write to temp file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(build_inst)

        # Run build script
        child = subprocess.Popen(
            'chmod +x %s && %s' % (f.name, f.name),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable='/bin/bash')
        output, errors = child.communicate()
        return_code = child.returncode

        # Failed build (update status)
        if return_code != 0:
            logging.warning('Build failed! See output for details')
            release.release_status_id = STATUS_FAILED

        # Good build (update status, move deb, create github release)
        else:
            logging.info('Build succeeded!')
            release.release_status_id = STATUS_IN_QA
            shutil.move('%s/build/%s_%s.deb' % (
                build_dir,
                app.name,
                release.version), Application.QA_PKG_DIR)
            self.rebuild_packages(Application.QA_PKG_DIR)
            '''
            Github.post('/repos/%s/%s/releases' % (app.github_owner, app.github_repo),
                params = {
                    'tag_name': 'v%s' % release.version,
                    'name': 'v%s' % release.version,
                    'target_commitish': release.tagged_branch,
                    'body': release.description
                }, access_token = user.access_token)
            '''

        # Clean up
        shutil.rmtree(build_dir)

        # Save
        release.build_output = 'Stdout:\n %s\n\n Stderr:\n%s' % (output, errors)
        release.save()

    def copy_to_prod(self, release):
        app = App(release.app_id)

        # Copy deb from qa to prod
        logging.info('Copying to prod %s v%s...' % (app.name, release.version))
        deb_path = '%s/%s_%s.deb' % (Application.QA_PKG_DIR, app.name, release.version)
        shutil.copy(deb_path, Application.PROD_PKG_DIR)
        self.rebuild_packages(Application.PROD_PKG_DIR)

        # Update release status
        release.release_status_id = STATUS_IN_PROD
        release.save()

    def rebuild_packages(self, pkg_dir):
        child = subprocess.Popen(
            'cd %s && dpkg-scanpackages . /dev/null | gzip -9c > %s/Packages.gz' % (
                pkg_dir, pkg_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable='/bin/bash')
        output, errors = child.communicate()
