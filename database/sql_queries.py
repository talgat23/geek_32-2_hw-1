CREATE_USER_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS telegram_users
        (ID INTEGER PRIMARY KEY,
        TELEGRAM_ID INTEGER,
        USERNAME CHAR(50),
        FIRST_NAME CHAR(50),
        LAST_NAME CHAR(50)
        )
"""

START_INSERT_USER_QUERY = """INSERT INTO telegram_users VALUES (?,?,?,?,?)"""