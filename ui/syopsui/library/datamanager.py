import psycopg2
from psycopg2.extras import DictCursor

class DataManager(object):
    def __init__(self, config):

        # Setup db
        dsn = "host=%s dbname=%s user=%s password=%s port=%s" % (
            config.get('db', 'host'),
            config.get('db', 'name'),
            config.get('db', 'username'),
            config.get('db', 'password'),
            config.get('db', 'port')
        )
        self.db = psycopg2.connect(dsn)
        self.db.autocommit = True
        self.db_cursor = self.db.cursor(cursor_factory=DictCursor)

    def get_db(self):
        return self.db

    def get_db_cursor(self):
        return self.db_cursor

    def cleanup(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()
