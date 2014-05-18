import json
import boto.sqs
from boto.sqs.message import Message

from syops.lib.application import Application
from syops.ui.models import Abstract
from syops.ui.models.app import App

class Release(Abstract):

    def __init__(self, data={}):
        self.app_id = data.get('app_id')
        self.branch = data.get('branch')
        self.version = data.get('version')
        self.description = data.get('description')

    def create(self):
        sqs = boto.sqs.connect_to_region(
            'us-east-1',
            aws_access_key_id=Application.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Application.AWS_SECRET_ACCESS_KEY)
        queue = sqs.get_queue('syops-releases')
        message = Message()

        # Build message payload
        payload = {
            'app_id': self.app_id,
            'branch': self.branch,
            'environment': 'qa',
            'version': self.version,
            'description': self.description,
        }

        # Add to queue
        message.set_body(json.dumps(payload))
        queue.write(message)
        return message.id
