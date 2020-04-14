import sqlite3
import os


def extract(lst):
    return list(map(lambda el: el[0], lst))


class SQLighter:

    def __init__(self):
        self.db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.db')
        try:
            with sqlite3.connect(self.db_file) as db:
                dbcursor = db.cursor()
                dbcursor.execute("""CREATE TABLE "users" (
                                    "telegram_id"	INTEGER NOT NULL UNIQUE,
                                    "current_state"	INTEGER DEFAULT 0,
                                    "last_saved_longitude"	REAL,
                                    "last_saved_latitude"	REAL,
                                    "daily_forecast_time"	TEXT,
                                    "time_offset"	INTEGER DEFAULT 0,
                                    PRIMARY KEY("telegram_id")
                                    );""")
                db.commit()
        except sqlite3.OperationalError:
            pass

    def add_new_user(self, telegram_id):
        with sqlite3.connect(self.db_file) as db:
            dbcursor = db.cursor()
            dbcursor.execute('INSERT INTO users (telegram_id) VALUES (?)', (telegram_id,))
            db.commit()

    def set_user_state(self, state, telegram_id, ):
        with sqlite3.connect(self.db_file) as db:
            dbcursor = db.cursor()
            dbcursor.execute('UPDATE users SET current_state = (?) WHERE telegram_id = (?)', (state, telegram_id,))
            db.commit()

    def get_current_state(self, telegram_id):
        with sqlite3.connect(self.db_file) as db:
            return db.cursor().execute('SELECT current_state FROM users WHERE telegram_id = (?)',
                                    (telegram_id,)).fetchone()[0]

    def update_coords(self, latitude, longitude, telegram_id):
        with sqlite3.connect(self.db_file) as db:
            dbcursor = db.cursor()
            dbcursor.execute("""UPDATE users 
                                SET last_saved_latitude = (?), last_saved_longitude = (?)
                                WHERE telegram_id = (?)""", (latitude, longitude, telegram_id,))
            db.commit()

    def get_current_coords(self, telegram_id):
        with sqlite3.connect(self.db_file) as db:
            return db.cursor().execute("""SELECT last_saved_latitude,
                                              last_saved_longitude
                                       FROM users
                                       WHERE telegram_id = (?)""",
                                      (telegram_id,)).fetchone()

    def update_time(self, time, telegram_id):
        with sqlite3.connect(self.db_file) as db:
            dbcursor = db.cursor()
            dbcursor.execute("""UPDATE users 
                                SET daily_forecast_time = (?)
                                WHERE telegram_id = (?)""", (time, telegram_id,))
            db.commit()

    def remove_user_time(self, telegram_id):
        try:
            with sqlite3.connect(self.db_file) as db:
                dbcursor = db.cursor()
                dbcursor.execute("""UPDATE users 
                                    SET daily_forecast_time = NULL
                                    WHERE telegram_id = (?)""", (telegram_id,))
                db.commit()
        except:
            pass

    def reset_user(self, telegram_id):
        with sqlite3.connect(self.db_file) as db:
            dbcursor = db.cursor()
            dbcursor.execute("""DELETE FROM users
                                WHERE telegram_id = (?)""", (telegram_id,))
            db.commit()

    def get_all_users(self):
        try:
            with sqlite3.connect(self.db_file) as db:
                return extract(db.cursor().execute('SELECT telegram_id FROM users',).fetchall())
        except TypeError:
            pass

    def get_all_times(self):
        try:
            with sqlite3.connect(self.db_file) as db:
                return extract(db.cursor().execute('SELECT daily_forecast_time FROM users',).fetchall())
        except TypeError:
            pass

    def get_users_by_time(self, time):
        with sqlite3.connect(self.db_file) as db:
            return extract(db.cursor().execute('SELECT telegram_id FROM users WHERE daily_forecast_time = (?)',
                           (time,)).fetchall())

    def get_time_by_user(self, user):
        try:
            with sqlite3.connect(self.db_file) as db:
                return extract(db.cursor().execute('SELECT daily_forecast_time FROM users WHERE telegram_id = (?)',
                               (user,)).fetchone())
        except TypeError:
            return None

    def update_time_offset(self, time_offset, telegram_id):
        with sqlite3.connect(self.db_file) as db:
            dbcursor = db.cursor()
            dbcursor.execute("""UPDATE users 
                                SET time_offset = (?)
                                WHERE telegram_id = (?)""", (time_offset, telegram_id,))
            db.commit()

    def get_time_offset(self, telegram_id):
        with sqlite3.connect(self.db_file) as db:
            return db.cursor().execute('SELECT time_offset FROM users WHERE telegram_id = (?)',
                                    (telegram_id,)).fetchone()[0]