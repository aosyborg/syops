import os.path
import time
import re
import glob
import boto.sqs

from syops.lib.models import Abstract
from syops.lib.models.app import App
from syops.lib.application import Application

class Debs(Abstract):

    def __init__(self, app):
        self.app = App(app) if app.isdigit() else app

    def get_latest_pkg(self, env='prod'):
        released = ''
        major = 0
        minor = 0
        revision = 0

        if env == 'prod':
            path = Application.PROD_PKG_DIR
        elif env == 'qa':
            path = Application.QA_PKG_DIR
        else:
            raise Exception('Unknown env')

        packages = glob.glob('%s/%s_*.deb' % (path, self.app.name))
        for package in packages:
            matches = re.search(r'_(\d+)\.(\d+)\-(\d+).deb', package)
            if not matches:
                continue

            if matches.group(1) >= major and \
                matches.group(2) >= minor and \
                matches.group(3) >= revision:
                major = matches.group(1)
                minor = matches.group(2)
                revision = matches.group(3)
                created = os.path.getctime(package)
                released = time.strftime('%Y-%m-%d', time.localtime(created))

        return {
            'released': released,
            'major': major,
            'minor': minor,
            'revision': revision
        }
