import sqlite3
from threading import Thread

con = sqlite3.connect('csf.db')


class DBSaver(Thread):
    def __init__(self, count, day_lot):
        Thread.__init__(self, name="DBSaver")
        self.count = count
        self.day_lot = day_lot

    def run(self):
        update_sql = 'UPDATE SETTING SET value = ? WHERE key = ?'
        update_data = [
            (self.count, 'count'),
            (self.day_lot, 'day_lot')
        ]

        with con:
            con.executemany(update_sql, update_data)


def fetch_count_and_day_lot():
    global con
    day_lot = 0
    count = 0
    with con:
        settings_data = con.execute("SELECT * FROM SETTING")
        for row in settings_data:
            if row[0] == 'day_lot':
                day_lot = int(row[1])
            if row[0] == 'count':
                count = int(row[1])
    return count, day_lot


def save_count_and_day_lot(count, day_lot):
    DBSaver(count, day_lot).start()


def reset_count_and_day_lot(count=0, day_lot=0):
    DBSaver(count, day_lot).run()


with con:
    # Create Structure
    try:
        con.execute("""
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
        con.executemany(sql, data)
    except sqlite3.IntegrityError:
        print("csf_db.py:Key already exists:")
