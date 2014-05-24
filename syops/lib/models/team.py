from hashlib import sha1
from syops.lib.models import Abstract
from syops.lib.application import Application

class Team(Abstract):

    def __init__(self, team_id=None, data={}):

        # Pull from db if user_id was passed
        if team_id:
            db_cursor = self.data_manager.get_db_cursor()
            db_cursor.execute('''
                SELECT *
                FROM teams
                WHERE id = %(team_id)s::BIGINT
                LIMIT 1
            ''', { 'team_id': team_id })
            data = db_cursor.fetchone() or {}

        # Populate object
        self.id = data.get('id')
        self.owner_id = data.get('owner_id')
        self.user_id = data.get('user_id')
        self.name = data.get('name')
        self.is_organization = data.get('is_organization')
        self.insert_ts = data.get('insert_ts')

    @staticmethod
    def get_team_apps(user_id):
        db_cursor = Team.data_manager.get_db_cursor()
        db_cursor.execute("""
            SELECT t.id AS team_id, t.name AS team_name,
                   a.id AS app_id, a.name AS app_name
            FROM teams t
            JOIN team_users ts on t.id = ts.team_id
            LEFT JOIN apps a on t.id = a.team_id
            WHERE ts.user_id = %(user_id)s::BIGINT;
        """, {'user_id': user_id})
        rows = db_cursor.fetchall()

        # Reorganize so its easier to work with
        teams = {}
        for row in rows:
            if row['team_id'] not in teams:
                teams[row['team_id']] = { 'name': row['team_name'], 'apps': {} }
            if row['app_id'] and row['app_id'] not in teams[row['team_id']]['apps']:
                teams[row['team_id']]['apps'][row['app_id']] = row['app_name']

        return teams

    def save(self):
        db_cursor = self.data_manager.get_db_cursor()
        db_cursor.execute('''
            SELECT * FROM set_team(%(id)s::BIGINT, %(name)s::VARCHAR,
                %(owner_id)s::BIGINT, %(is_org)s::BOOLEAN)
        ''', {
            'id': self.id,
            'name': self.name,
            'owner_id': self.owner_id,
            'is_org': self.is_organization,
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
            FROM teams
            WHERE id = %(team_id)s::BIGINT
        ''', { 'team_id': self.id })
        return True
