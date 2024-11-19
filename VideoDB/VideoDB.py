import sys
import signal
from flask import Flask
from flask import request
import json
from VideoIndexer import VideoIndexer
from VectorDB import VectorDB
from OpenAIEmbeddingsGenerator import OpenAIEmbeddingsGenerator

app = Flask(__name__)

embeddings_generator = OpenAIEmbeddingsGenerator("OPENAI_API_KEY")
db = VectorDB("./tmp/vector.db", embeddings_generator)
indexer = VideoIndexer(db)
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

@app.route('/add_caption')
def add_caption():
    url = request.args.get('url')
    caption = request.args.get('caption')
    timestamp = request.args.get('timestamp')
    if(url==None or caption==None):
        return '{}', 400
    
    try:
        db.add_row(url, caption, timestamp)
        return json.dumps({"success": True}), 200
    
    except ValueError as e:
        return '{}', 401
    except Exception as e:
        print(e)
        return '{}', 500

@app.route('/search')
def search():
    query = request.args.get('query')
    if(query==None):
        return '{}', 400
    try:
        return json.dumps(db.search_captions(query, 1)), 200
    
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