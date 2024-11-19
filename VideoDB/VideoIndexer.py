import threading
import time
from queue import Queue
from yt_dlp import YoutubeDL
# Handles multithreaded background jobs for indexing

class VideoIndexer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.jobs = Queue()
        self.running = True

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
            time.sleep(5)
            print("Indexing done")

    def kill_all(self):
        self.running = False
        with self.condition:
            self.condition.notify(10000)

    def get_subs(self, url):
        dlp_args = {
            'writeautomaticsub': True,
            'subtitlesformat': 'vtt',
            'skip_download': True,
            'outtmpl': './tmp/sub.vtt' 
        }
        with YoutubeDL(dlp_args) as ydl:
            a = ydl.download([url])
            print(a)

