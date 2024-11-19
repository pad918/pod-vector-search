import threading
import time
import os
from queue import Queue
from yt_dlp import YoutubeDL
from VectorDB import VectorDB
# Handles multithreaded background jobs for indexing

class VideoIndexer(threading.Thread):
    def __init__(self, db):
        super().__init__()
        self.jobs = Queue()
        self.running = True
        self.vector_db = db

    def add_job(self, url):
        print(f"Adding job: {url}")
        self.jobs.put(url)
        print(f"Total number of jobs: {self.jobs.qsize()}")
        

    def run(self):
        # Handle one job at the time
        while self.running:
            url = self.jobs.get(True)
            if not self.running:
                break  
            print("Indexing video: " + url)
            
            # Download the subtitles
            subs = self.get_subs(url)
            if(subs == None):
                print("Could not get subtitles")
                continue

            # Add to DB

            print("Found subs: " + subs)

            print("Indexing done")

    def kill_all(self):
        self.running = False
        # Add to queue for the threads to stop blocking
        # To improve the code, a special job called KILL_THREAD
        # Can be added to the queue
        for i in range(1):
            self.jobs.put(None)

    def get_subs(self, url):
        dlp_args = {
            'writeautomaticsub': True,
            'subtitlesformat': 'vtt',
            'skip_download': True,
            'outtmpl': './tmp/subs' 
        }
        try:
            with YoutubeDL(dlp_args) as ydl:
                # Download subtitles a temp file (can not be read directly)
                a = ydl.download([url])
                
                # Read the text in the temp file
                with open('./tmp/subs.en.vtt', 'r') as f:
                    subs = f.read()
                
                # Remove temp file
                os.remove('./tmp/subs.en.vtt')
                return subs
        except Exception as e:
            print(e)
            os.remove('./tmp/subs.en.vtt')
            return None
        

