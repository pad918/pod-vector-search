import sqlite3
import struct
from typing import List
import sqlite_vec
from EmbeddingGenerator import EmbeddingGenerator

class VectorDB:
    def __init__(self, db_path, embeddings_generator:EmbeddingGenerator):
        self.embeddings_generator = embeddings_generator

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
                caption TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )''')
        
        # Table with added videos
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS videos(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
                origin_url TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL
            )''')

        # Vector view / virtual table
        self.db.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS caption_vectors 
                USING vec0(embedding float[1536])
            ''')
        self.db.commit()
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

    def add_row(self, origin_url:str, caption:str, timestamp:str, commit = True, vector = None):
        if(vector == None):
            vector = self.serialize_f32(self.embeddings_generator.generate_single_embedding(caption))
        
        self.db.execute('''
            INSERT INTO captions (origin_url, caption, timestamp) 
                VALUES (?,?,?)
            ''', (origin_url, caption, timestamp))
        
        seq_num = self.get_last_seq_num()
        
        self.db.execute('''
            INSERT INTO caption_vectors (rowid, embedding) 
                VALUES (?,?)
            ''', (seq_num, vector))
        if commit:
            self.db.commit()
    
    def add_captions(self, origin_url:str, captions:List[str], timestamps:List[str]):
        # Use batching to speed up embedding computation (the slowest part of indexing)
        def as_batch(lst, batch_size):
            for i in range(0, len(lst), batch_size):
                yield lst[i:i + batch_size]

        batches = as_batch([(c,t) for c,t in zip(captions, timestamps)], 100)

        # Add all captions, and commit when all have been added
        for batch in batches:
            batch_captions   = [caption for caption, _ in batch]
            batch_timestamps = [timestamp for _, timestamp in batch]
            raw_vectors = self.embeddings_generator.generate_batch_embedding([caption for caption in batch_captions])
            vectors = [self.serialize_f32(v) for v in raw_vectors]
            for caption, timestamp, vector in zip(batch_captions, batch_timestamps, vectors):
                self.add_row(origin_url, caption, timestamp, commit=False, vector=vector)

        # Add video to videos table
        self.db.execute('''
            INSERT INTO videos (origin_url, status) 
            VALUES (?,?)
            ''', (origin_url, "indexed"))
        
        self.db.commit()
        

    def search_captions(self, query:str, limit:int = 5):
        row_ids = self.get_close_vectors(query, limit)
        print(f"found: {len(row_ids)} rows")
        # Remove the distance field
        row_ids = [r[0] for r in row_ids]
        
        # Find the corresponding rows in the captions table
        return [self.get_row_with_id(id) for id in row_ids]

    def get_close_vectors(self, caption:str, limit:int = 5):
        vector = self.serialize_f32(self.embeddings_generator.generate_single_embedding(caption))
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