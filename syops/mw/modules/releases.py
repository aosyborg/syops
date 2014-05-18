import logging
import json
import boto.sqs
from boto.sqs.message import Message

from syops.mw.modules import Abstract

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

    def create(self, params={}):
        environment = params.get('environment')
        version = params.get('version')
        app_id = params.get('app_id')
        branch = params.get('branch')
        description = params.get('description')
