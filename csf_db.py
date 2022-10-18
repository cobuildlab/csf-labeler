import sqlite3
from threading import Thread

connection = None
is_loaded = False


def _save_count_and_day_lot(count, day_lot):
    global connection
    update_sql = 'UPDATE SETTING SET value = ? WHERE key = ?'
    update_data = [
        (count, 'count'),
        (day_lot, 'day_lot')
    ]

    with connection:
        connection.executemany(update_sql, update_data)


def fetch_count_and_day_lot():
    global is_loaded
    if is_loaded is False:
        global connection
        connection = sqlite3.connect('csf.db')
        _init_database(connection)
        is_loaded = True

    day_lot = 0
    count = 0
    with connection:
        settings_data = connection.execute("SELECT * FROM SETTING")
        for row in settings_data:
            if row[0] == 'day_lot':
                day_lot = int(row[1])
            if row[0] == 'count':
                count = int(row[1])
    return count, day_lot


def save_count_and_day_lot(count, day_lot):
    _save_count_and_day_lot(count, day_lot)


def reset_count_and_day_lot(count=0, day_lot=0):
    _save_count_and_day_lot(count, day_lot)


def _init_database(local_connection):
    with local_connection:
        # Create Structure
        try:
            local_connection.execute("""
                CREATE TABLE SETTING (
                    key TEXT NOT NULL PRIMARY KEY,
                    value TEXT
                );
            """)
        except sqlite3.OperationalError:
            print("csf_db.py:SETTING table already exists")

        # Insert initial values
        sql = 'INSERT INTO SETTING (key, value) values( ?, ?)'
        data = [
            ('count', '0'),
            ('day_lot', '0')
        ]
        try:
            local_connection.executemany(sql, data)
        except sqlite3.IntegrityError:
            print("csf_db.py:Key already exists:")
