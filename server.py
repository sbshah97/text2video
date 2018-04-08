from gevent import monkey
import json
from flask import Flask, request, Response, render_template, abort, url_for
import gevent
import requests
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'webapp/pdf'
ALLOWED_EXTENSIONS = set(['pdf'])

# Flask Variables
app = Flask(__name__)
monkey.patch_all()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
subscription_key = "5ecd1122df704d5080f7a4639f1aad98"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             print('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             print('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <p><input type=file name=file>
#          <input type=submit value=Upload>
#     </form>
#     '''

@app.route('/upload', methods=['GET'])
def upload_page():
   return render_template('upload.html')


@app.route('/pdf_upload', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
      return 'File Uploaded Successfully'


@app.route('/')
def index():
    return render_template('index.html', name='Code Fun Do')

# Main Method in the Server code
if __name__ == '__main__':
    # Set server address 0.0.0.0:5000/
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
