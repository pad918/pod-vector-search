from AuthConnector import AuthConnector
import sqlite3


class SQLiteAuthConnector(AuthConnector):
    def __init__(self, database_name):
        self.con = sqlite3.connect(database_name, check_same_thread=False)
        cur = self.con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users 
                    (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
                    username TEXT UNIQUE NOT NULL, 
                    password_hash TEXT NOT NULL
                    )''')
        self.con.commit()

    def __del__(self):
        self.con.close()

    def get_hash(self, username):
        cur = self.con.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username=?", (username,))
        result = cur.fetchone()
        if result == None: raise ValueError(f"Did not find any hash entry for user: {username}")
        if len(result) != 1: raise ValueError(f"Found multiple hash entries for user: {username}")
        return result[0]

    def register_user(self, username, hash):
        cur = self.con.cursor()
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?,?)", (username, hash))
        self.con.commit()

