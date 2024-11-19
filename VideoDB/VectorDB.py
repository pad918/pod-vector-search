import sqlite3
import struct
from typing import List
import sqlite_vec

class VectorDB:
    def __init__(self, db_path):
        # Load vector extension
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self.db.enable_load_extension(True)
        sqlite_vec.load(self.db)
        self.db.enable_load_extension(False)

        # Create table
        self.create_inital_db()

        
    
    def create_inital_db(self):
        
        # Main data table
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS captions(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
                origin_url TEXT NOT NULL, 
                caption TEXT NOT NULL
            )''')
        
        # Vector view / virtual table
        self.db.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS caption_vectors 
                USING vec0(embedding float[1536])
            ''')
            
        print("Created new vector db with vector index")
    
    
    def serialize_f32(self, vector: List[float]) -> bytes:
        return struct.pack("%sf" % len(vector), *vector)

    def get_last_seq_num(self):
        seqnum = self.db.execute('''
            SELECT seq from sqlite_sequence where name='captions'
            ''').fetchone()[0]
        print(f"seqnum = {seqnum}")
        return seqnum

    def get_row_with_id(self, row_id:int):
        return self.db.execute('''
            SELECT * FROM captions WHERE id = ?
            ''', (row_id,)).fetchone()

    def add_row(self, origin_url:str, caption:str, timestamp):
        vectors = self.serialize_f32([i/1535.0 for i in range(1536)])
        
        self.db.execute('''
            INSERT INTO captions (origin_url, caption) 
                VALUES (?,?)
            ''', (origin_url, caption))
        
        seq_num = self.get_last_seq_num()
        
        self.db.execute('''
            INSERT INTO caption_vectors (rowid, embedding) 
                VALUES (?,?)
            ''', (seq_num, vectors))
    
    def search_captions(self, query:str, limit:int = 5):
        row_ids = self.get_close_vectors(query, limit)
        
        # Remove the distance field
        row_ids = [r[0] for r in row_ids]
        
        # Find the corresponding rows in the captions table
        return [self.get_row_with_id(id) for id in row_ids]

    def get_close_vectors(self, caption:str, limit:int = 5):
        vector = self.serialize_f32([i/1535.0 for i in range(1536)])
        
        result = self.db.execute('''
            SELECT
        rowid,
        distance
        FROM caption_vectors
        WHERE embedding MATCH ?
        ORDER BY distance
        LIMIT ?
            ''', (vector, limit)).fetchall()
        return result