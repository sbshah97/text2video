from gevent import monkey
import json
from flask import Flask, request, Response, render_template, abort, url_for, redirect
import gevent
import requests
import mysql
import os
import subprocess
import time
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'webapp/pdf'
ALLOWED_EXTENSIONS = set(['pdf'])

# Flask Variables
app = Flask(__name__, static_folder='webapp/')
monkey.patch_all()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
subscription_key = "5ecd1122df704d5080f7a4639f1aad98"


# Helper method to get timestamp for a particular class
def get_timestamp():
    return int(time.time() * 1000000)


@app.route('/user_register', methods=['POST'])
def user_register():
    print(request.form)
    mysql.commit('insert into Users(username, password) values ("{0}", "{1}")'.format(
        request.form['username'],
        request.form['password']
    ))
    return 'Success'


@app.route('/user_login', methods=['POST'])
def user_login():
    print(request.form)
    users = mysql.fetch_all('select * from Users where username = "{0}" and password = "{1}"'.format(
        request.form['username'],
        request.form['password']
    ))
    if len(users) != 1:
        return 'Fail'
    return str(users[0][0])


@app.route('/get_videos', methods=['POST'])
def get_videos():
    print(request.form)
    videos = mysql.fetch_all('select * from Videos where user_id = {0}'.format(request.form['id']))
    data = []
    for video in videos:
        data.append({
            'video_file': video[1],
            'summary_file': video[2],
            'q_file': video[3],
            'time': video[4],
        })
    return json.dumps(data)


@app.route('/fetch_video', methods=['GET'])
def fetch_video():
    print "he"
    file = request.args.get('v')
    print file
    print os.listdir('webapp/vid')
    if file not in os.listdir('webapp/vid'):
        return app.send_static_file('pending.html')
    return app.send_static_file('vid/' + file)


@app.route('/try', methods=['POST'])
def try_():
    user_id = request.form['id']
    print user_id
    text = request.form['text']
    timestamp = get_timestamp()
    text_file = 'tmp/tmp{0}.txt'.format(timestamp)
    file = open(text_file, 'w')
    file.write(text)
    file.close()
    subprocess.Popen(['python driver.py ' + str(timestamp) + ' ' + text_file], shell=True)
    print 'insert into Videos values({0}, "{1}", "{2}", "{3}", {4})'.format(
        user_id,
        'vid/vid{0}.mp4'.format(timestamp),
        'sum/sum{0}.txt'.format(timestamp),
        'q/q{0}.txt'.format(timestamp),
        timestamp
    )
    mysql.commit('insert into Videos values({0}, "{1}", "{2}", "{3}", {4})'.format(
        user_id,
        'vid{0}.mp4'.format(timestamp),
        'sum/sum{0}.txt'.format(timestamp),
        'q/q{0}.txt'.format(timestamp),
        int(timestamp/1000)
    ))
    return "Success"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/pdf_upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print  request.files['file']
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        return 'File Uploaded Successfully'


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


mysql.PASS = raw_input("MYSQL root password? ")
# Main Method in the Server code
if __name__ == '__main__':
    # Set server address 0.0.0.0:5000/
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
