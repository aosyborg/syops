import json
import boto.sqs
from boto.sqs.message import Message

from syops.lib.application import Application
from syops.lib.models import Abstract
from syops.lib.models.app import App

class Release(Abstract):

    def __init__(self, release_id=None, data={}):
        # Pull from db if release_id was passed
        if release_id:
            db_cursor = self.data_manager.get_db_cursor()
            db_cursor.execute('''
                SELECT * FROM releases WHERE id = %(id)s::BIGINT LIMIT 1
            ''', { 'id': release_id })
            data = db_cursor.fetchone() or {}

        self.id = data.get('id')
        self.app_id = data.get('app_id')
        self.release_status_id = data.get('release_status_id', 1)
        self.status = data.get('status', 1)
        self.version = data.get('version')
        self.tagged_branch = data.get('tagged_branch')
        self.description = data.get('description')
        self.build_output = data.get('build_output')
        self.update_ts = data.get('update_ts')
        self.insert_ts = data.get('insert_ts')

    def save(self, user_id=None):
        sqs = boto.sqs.connect_to_region(
            'us-east-1',
            aws_access_key_id=Application.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Application.AWS_SECRET_ACCESS_KEY)
        queue = sqs.get_queue(Application.RELEASE_QUEUE)
        message = Message()

        # Add to release table
        db_cursor = self.data_manager.get_db_cursor()
        db_cursor.execute('''
            SELECT * FROM set_release(%(id)s::BIGINT, %(app_id)s::BIGINT,
                %(release_status_id)s::INTEGER, %(version)s::VARCHAR,
                %(tagged_branch)s::VARCHAR, %(description)s::TEXT, %(build_output)s::TEXT)
        ''', {
            'id': self.id,
            'app_id': self.app_id,
            'release_status_id': self.release_status_id,
            'version': self.version,
            'tagged_branch': self.tagged_branch,
            'description': self.description,
            'build_output': self.build_output
        })
        row = db_cursor.fetchone()

        # If user_id was passed, add to message queue
        if user_id:
            # Build message payload
            payload = {
                'release_id': row[0],
                'user_id': user_id
            }

            # Add to queue
            message.set_body(json.dumps(payload))
            queue.write(message)
        return message.id

    @staticmethod
    def get_list(app_id):
        db_cursor = Release.data_manager.get_db_cursor()
        db_cursor.execute("""
            SELECT r.*, rs.name as status
            FROM releases r
            JOIN release_statuses rs ON r.release_status_id = rs.id
            WHERE r.app_id = %(app_id)s::BIGINT
            ORDER BY r.id DESC
        """, {'app_id': app_id})
        rows = db_cursor.fetchall()

        return rows if rows else []

    @staticmethod
    def get_latest(app_id):
        db_cursor = Release.data_manager.get_db_cursor()
        db_cursor.execute('''
            SELECT r.*, rs.name as status
            FROM releases r
            JOIN release_statuses rs ON r.release_status_id = rs.id
            WHERE r.app_id = %(app_id)s::BIGINT
            AND r.release_status_id > 1
            ORDER BY update_ts DESC
            LIMIT 1
        ''', {
            'app_id': app_id
        })
        row = db_cursor.fetchone()
        return Release(data=row) if row else False
