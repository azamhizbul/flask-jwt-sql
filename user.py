import sqlite3

from connectionDB import connect

class User(object):
    TABLE_NAME = 'user'
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        with connect():
            cur = connect().cursor()
            query = "SELECT * FROM {table} WHERE username=?".format(table=cls.TABLE_NAME)
            
            result = cur.execute(query, (username,))
            row = result.fetchone()
            if row:
                user = cls(*row)
            else:
                user = None

            cur.close()
            return user

    @classmethod
    def find_by_id(cls, _id):
        with connect():
            cur = connect().cursor()
            query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
            result = cur.execute(query, (_id,))
            row = result.fetchone()
            if row:
                user = cls(*row)
            else:
                user = None

            cur.close()
            return user    