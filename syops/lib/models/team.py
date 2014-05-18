from hashlib import sha1
from syops.lib.models import Abstract
from syops.lib.application import Application

class Team(Abstract):

    def __init__(self, team_id=None, data={}):

        # Pull from db if user_id was passed
        if team_id:
            db_cursor = self.data_manager.get_db_cursor()
            db_cursor.execute('''
                SELECT id, user_id as owner_id, name, insert_ts
                FROM teams
                WHERE id = %(team_id)s::BIGINT
                LIMIT 1
            ''', { 'team_id': team_id })
            data = db_cursor.fetchone() or {}

        # Populate object
        self.id = data.get('id')
        self.owner_id = data.get('owner_id')
        self.name = data.get('name')
        self.insert_ts = data.get('insert_ts')

    @staticmethod
    def get_list(user_id):
        db_cursor = Team.data_manager.get_db_cursor()
        db_cursor.execute("""
            SELECT t.id as team_id, t.name as team_name, t.insert_ts as created,
                   u.id as owner_id, u.name as owner_name,
                   tmp.count as member_count
            FROM teams t
            LEFT JOIN team_users ts ON t.id = ts.team_id
            JOIN users u ON ts.user_id = u.id
            JOIN (SELECT team_id, COUNT(*) AS count FROM team_users GROUP BY team_id) AS tmp
                ON tmp.team_id = t.id
            WHERE ts.user_id = %(user_id)s::BIGINT
        """, {'user_id': user_id})
        rows = db_cursor.fetchall()

        return rows if rows else []

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
                %(owner_id)s::BIGINT)
        ''', {
            'id': self.id,
            'name': self.name,
            'owner_id': self.owner_id
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
