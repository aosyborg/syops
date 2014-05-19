from hashlib import sha1
from syops.lib.models import Abstract
from syops.lib.application import Application

class App(Abstract):

    def __init__(self, app_id=None, data={}):

        # Pull from db if app_id was passed
        if app_id:
            db_cursor = self.data_manager.get_db_cursor()
            db_cursor.execute('''
                SELECT *
                FROM apps
                WHERE id = %(app_id)s::BIGINT
                LIMIT 1
            ''', { 'app_id': app_id })
            data = db_cursor.fetchone() or {}

        # Populate object
        self.id = data.get('id')
        self.team_id = data.get('team_id')
        self.name = data.get('name')
        self.clone_url = data.get('clone_url')
        self.github_owner = data.get('github_owner')
        self.github_repo = data.get('github_repo')
        self.build_instructions = data.get('build_instructions')
        self.insert_ts = data.get('insert_ts')

    @staticmethod
    def get_list(team_id):
        db_cursor = App.data_manager.get_db_cursor()
        db_cursor.execute("""
            SELECT *
            FROM apps a
            WHERE a.team_id = %(team_id)s::BIGINT
        """, {'team_id': team_id})
        rows = db_cursor.fetchall()

        return rows if rows else []

    def save(self):
        db_cursor = self.data_manager.get_db_cursor()
        db_cursor.execute('''
            SELECT * FROM set_app(%(id)s::BIGINT, %(team_id)s::BIGINT,
                %(name)s::VARCHAR, %(clone_url)s::VARCHAR, %(github_owner)s::VARCHAR,
                %(github_repo)s::VARCHAR, %(build_instructions)s::TEXT)
        ''', {
            'id': self.id,
            'team_id': self.team_id,
            'name': self.name,
            'clone_url': self.clone_url,
            'github_owner': self.github_owner,
            'github_repo': self.github_repo,
            'build_instructions': self.build_instructions,
        })
        row = db_cursor.fetchone()
        # Repopulate the object after successful save
        self.__init__(row[0])

    def delete(self):
        if not self.id:
            return False

        db_cursor = self.data_manager.get_db_cursor()
        db_cursor.execute('''
            DELETE
            FROM apps
            WHERE id = %(app_id)s::BIGINT
        ''', { 'app_id': self.id })
        return True
