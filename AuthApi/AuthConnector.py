import sqlite3
# Connects to the database

class AuthConnector:
    def __init__(self, database_name):
        self.con = sqlite3.connect(database_name)

    def __del__(self):
        self.con.close()
    
    def get_hash(self, username):
        raise NotImplementedError
    
    def register_user(self, username, hash):
        raise NotImplementedError
    
    def add_token(self, username, lifespan):
        raise NotImplementedError
    
    def get_tokens(self, username):
        raise NotImplementedError