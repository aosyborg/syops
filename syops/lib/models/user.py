from hashlib import sha1
from syops.lib.models import Abstract
from syops.lib.application import Application
from syops.lib.models.team import Team
from syops.lib.models.github import Github

class User(Abstract):

    def __init__(self, user_id=None, data={}):

        # Pull from db if user_id was passed
        if user_id:
            db_cursor = self.data_manager.get_db_cursor()
            db_cursor.execute('''
                SELECT *
                FROM users
                WHERE id = %(user_id)s::BIGINT
                LIMIT 1
            ''', { 'user_id': user_id })
            data = db_cursor.fetchone() or {}

        # Populate object
        self.id = data.get('id')
        self.name = data.get('name')
        self.email = data.get('email')
        self.access_token = data.get('access_token')
        self.avatar_url = data.get('avatar_url')
        self.is_verified = data.get('is_verified', False)
        self.is_admin = data.get('is_admin', False)
        self.insert_ts = data.get('insert_ts')

    @staticmethod
    def build_from_email(email):
        db_cursor = User.data_manager.get_db_cursor()
        db_cursor.execute("""
            SELECT id FROM users WHERE email = %(email)s::VARCHAR LIMIT 1
        """, {'email': email})
        row = db_cursor.fetchone()
        return User(row['id']) if row else False

    @staticmethod
    def build_from_access_token(access_token):
        user_info = Github.get('/user', access_token=access_token)
        if not user_info:
            return False

        # Attempt to query for user based on email
        db_cursor = User.data_manager.get_db_cursor()
        db_cursor.execute("""
            SELECT id FROM users WHERE email = %(email)s::VARCHAR AND is_verified = True
        """, {'email': user_info.get('email')})
        row = db_cursor.fetchone()

        # If not verified (registered) user, they shall not pass
        if not row:
            return False

        # Instantiate user and set access token
        user = User(row['id'])
        user.name = user_info.get('name')
        user.avatar_url = user_info.get('avatar_url')
        user.access_token = access_token
        return user.save()

    def save(self):
        db_cursor = self.data_manager.get_db_cursor()
        db_cursor.execute('''
            SELECT * FROM set_user(%(id)s::BIGINT, %(email)s::VARCHAR,
                %(name)s::VARCHAR, %(access_token)s::VARCHAR, %(avatar_url)s::VARCHAR,
                %(is_verified)s::BOOLEAN, %(is_admin)s::BOOLEAN)
        ''', {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'access_token': self.access_token,
            'avatar_url': self.avatar_url,
            'is_verified': self.is_verified,
            'is_admin': self.is_admin
        })
        row = db_cursor.fetchone()

        # If this is a new user, create a team for them
        if not self.id or self.id != row[0]:
            team = Team()
            team.owner_id = row[0]
            team.name = 'My projects'
            team.save()

        # Repopulate the object after successful save
        self.__init__(row[0])
        return self

    def delete(self):
        if not self.id:
            return False

        # Ensure user isn't an owner of any teams
        db_cursor = self.data_manager.get_db_cursor()
        db_cursor.execute('''
            SELECT *
            FROM teams
            WHERE user_id = %(user_id)s::BIGINT
            LIMIT 1
        ''', { 'user_id': self.id })
        row = db_cursor.fetchone()
        if row:
            return False

        # Delete the actual user (will cascade)
        db_cursor.execute('''
            DELETE
            FROM users
            WHERE id = %(user_id)s::BIGINT
        ''', { 'user_id': self.id })
        return True
