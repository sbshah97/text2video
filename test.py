from flask import Flask, render_template, request
from werkzeug import secure_filename
import os

app = Flask(__name__, static_folder='webapp/')
UPLOAD_FOLDER = 'webapp/pdf'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload')
def upload_html():
   return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
      return 'file uploaded successfully'


if __name__ == '__main__':
   app.run(debug=True)
