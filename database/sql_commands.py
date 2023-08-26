import sqlite3
from database import sql_queries

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite3")
        self.cursor = self.connection.cursor()
        self.sql_create_db()

    def sql_create_db(self):
        if self.connection:
            print("Database connected successfully")

        self.cursor.execute(sql_queries.CREATE_USER_TABLE_QUERY)
        self.connection.commit()


    def sql_insert_user_command(self, telegram_id, username,
                                first_name, last_name):
        self.cursor.execute(sql_queries.START_INSERT_USER_QUERY,
                            (None,
                             telegram_id,
                             username,
                             first_name,
                             last_name)
                            )
        self.connection.commit()