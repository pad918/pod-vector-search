import threading
import time
import os
import glob
import webvtt
from queue import Queue
from yt_dlp import YoutubeDL
from VectorDB import VectorDB
from pytube import Playlist
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
    
    def add_playlist(self, playlist_url):
        print(f"Adding playlist: {playlist_url}")
        playlist = Playlist(playlist_url)
        for video in playlist.videos:
            self.add_job(video.watch_url)

    def run(self):
        # Handle one job at the time
        while self.running:
            url = self.jobs.get(True)
            if not self.running:
                break  
            print("Indexing video: " + url)
            try:
                self.process_video(url)
            except Exception as e:
                print(e) # Handle failure here

            print("Indexing done")
    
    def process_video(self, url):
        # Download the subtitles
        vtt_string = self.get_subs(url)
        if(vtt_string == None):
            print("Could not get subtitles")
            raise Exception("Could not get subtitles")
        vtt = webvtt.from_string(vtt_string)

        # Add all the captions to the database
        captions = []
        timestamps = []
        last_timestamp = None
        curr_cap = ""
        last = ""
        for caption in vtt:
            next = caption.text.strip()
            if(last_timestamp == None):
                last_timestamp = caption.start
            if(next.startswith(last)):
                to_add = next[len(last):].strip()
                curr_cap += " " + to_add
            elif(last.endswith(next) or next == last):
                pass
            else:
                curr_cap += " " + next
            if(len(curr_cap) >= 100):
                #print(f"Added caption: {curr_cap}")
                captions.append(curr_cap)
                timestamps.append(str(last_timestamp))
                curr_cap = ""
                last_timestamp = None
            last = next

        print(f"Found: {len(captions)} captions, adding to db... estimated time = {len(captions)}s")   
        self.vector_db.add_captions(url, captions, timestamps)

    def kill_all(self):
        self.running = False
        # Add to queue for the threads to stop blocking
        # To improve the code, a special job called KILL_THREAD
        # Can be added to the queue
        for i in range(1):
            self.jobs.put(None)

    def get_subs(self, url):
        dlp_args = {
            'writeautomaticsub': False,
            'writesubtitles': True,
            'subtitlesformat': 'vtt',
            'skip_download': True,
            'outtmpl': './tmp/subs' 
        }
        try:
            with YoutubeDL(dlp_args) as ydl:
                # Download subtitles as a temp file (can not be read directly)
                ydl.download([url])
                
                # Find the temp file
                files = glob.glob('./tmp/subs*en*.vtt')
                if(len(files) == 0 or len(files) > 1):
                    raise Exception(f"Could not find temp file for video: {url}")
                subs_file = files[0]

                # Read the text in the temp file
                with open(subs_file, 'r') as f:
                    subs = f.read()
                
                # Remove temp file
                os.remove(subs_file)
                return subs
        except Exception as e:
            print(e)
            os.remove(subs_file)
            return None
        

