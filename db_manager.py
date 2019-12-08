import sqlite3
import os


class SQLighter:

    def __init__(self):
        self.db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.db')

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
            dbcursor = db.cursor()
            return dbcursor.execute('SELECT current_state FROM users WHERE telegram_id = (?)',
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
            dbcursor = db.cursor()
            return dbcursor.execute("""SELECT last_saved_latitude,
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

    def reset(self, telegram_id):
        with sqlite3.connect(self.db_file) as db:
            dbcursor = db.cursor()
            dbcursor.execute("""DELETE FROM users
                                WHERE telegram_id = (?)""", (telegram_id,))
            db.commit()
