import logging
import json
import subprocess
import boto.sqs
from httplib2 import Http
from urllib import urlencode
from boto.sqs.message import Message

from syops.mw.modules import Abstract
from syops.lib.models.app import App

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
            payload = message.get_body()
            logging.info('Release info recieved: %s' % payload)
            self.create(json.loads(payload))
            #self.queue.delete_message(message)

    def create(self, params={}):
        environment = params.get('environment')
        version = params.get('version')
        app_id = params.get('app_id')
        branch = params.get('branch')
        description = params.get('description')

        # Build app object
        app = App(app_id)
        if not app.id:
            logging.error('No app id found!')
            return

        # Tag in GitHub
        api_url = 'https://api.github.com'
        url = '%s/repos/%s/%s/releases' % (api_url, app.github_owner, app.github_repo)
        params = {
            'tag_name': 'v%s' % version,
            'target_commitish': branch,
            'name': 'v%s' % version,
            'body': description,
            'prerelease': True
        }
        headers, content = Http().request(url, 'POST', urlencode(params))
        print url
        print headers
        print content

    def build(self, app):
        # Run build instructions
        if app.build_instructions:
            child = subprocess.Popen(
                app.build_instructions,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True)
            output, errors = child.communicate()
            return_code = child.returncode

            print output, return_code
