import sys
import signal
from flask import Flask
from flask import request
import json
from VideoIndexer import VideoIndexer

app = Flask(__name__)
indexer = VideoIndexer()
indexer.start()


# TODO, require authentication ticket to add videos!
@app.route('/add_video')
def login():
    url = request.args.get('url')
    print(url)
    if(url==None):
        return '{}', 400
    try:
        indexer.add_job(url)
        return json.dumps({}), 200
    
    except ValueError as e:
        return '{}', 401
    except Exception as e:
        print(e)
        return '{}', 500
    

def handler(signal, frame):
    indexer.kill_all()
    indexer.join()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)
#signal.pause()