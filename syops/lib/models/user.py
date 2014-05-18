from hashlib import sha1
from syops.lib.models import Abstract
from syops.lib.application import Application

class User(Abstract):

    def __init__(self, user_id=None, data={}):

        # Pull from db if user_id was passed
        if user_id:
            db_cursor = self.data_manager.get_db_cursor()
            db_cursor.execute('''
                SELECT id, name, email, is_admin, insert_ts
                FROM users
                WHERE id = %(user_id)s::BIGINT
                LIMIT 1
            ''', { 'user_id': user_id })
            data = db_cursor.fetchone() or {}

        # Populate object
        self.id = data.get('id')
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = data.get('password')
        self.is_admin = data.get('is_admin')
        self.insert_ts = data.get('insert_ts')

    @staticmethod
    def login(email, password):
        db_cursor = User.data_manager.get_db_cursor()
        password_hash = sha1('%s%s' % (Application.SALT, password)).hexdigest()
        db_cursor.execute("""
            SELECT id
            FROM users
            WHERE email = %(email)s::VARCHAR
            AND password = %(password)s::VARCHAR
            LIMIT 1
        """, {
            'email': email,
            'password': password_hash
        })
        row = db_cursor.fetchone()

        # Sanity check: if no user found simply return False
        if not row:
            return False

        # If a user was found build and return that object
        return User(row['id'])

    @staticmethod
    def get_list(offset=0):
        db_cursor = User.data_manager.get_db_cursor()
        db_cursor.execute("""
            SELECT id as user_id, name, email, is_admin, insert_ts
            FROM users
            OFFSET %(offset)s::INTEGER
            LIMIT 20
        """, { 'offset': offset })
        rows = db_cursor.fetchall()

        return rows if rows else []

    def save(self):
        db_cursor = self.data_manager.get_db_cursor()
        db_cursor.execute('''
            SELECT * FROM set_user(%(id)s::BIGINT, %(email)s::VARCHAR,
                %(password)s::VARCHAR, %(name)s::VARCHAR, %(is_admin)s::BOOLEAN)
        ''', {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'is_admin': self.is_admin
        })
        row = db_cursor.fetchone()
        # Repopulate the object after successful save
        self.__init__(row[0])

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
