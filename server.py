from gevent import monkey
import json
from flask import Flask, request, Response, render_template, abort, url_for
import gevent
import BingImages
import requests

# Flask Variables
app = Flask(__name__)
monkey.patch_all()

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
subscription_key = "5ecd1122df704d5080f7a4639f1aad98"


@app.route('/')
def index():
    return render_template('index.html', name='Code Fun Do')



# Main Method in the Server code
if __name__ == '__main__':
    # Set server address 0.0.0.0:5000/
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
