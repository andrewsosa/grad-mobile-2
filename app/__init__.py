import os, thread

from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'storage'
ALLOWED_EXTENSIONS = set(['wav', 'txt'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.url_map.strict_slashes = False

#
#   UTIL
#

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#
#   DATA STORE
#

sensorData = dict()


#
#   ROUTES
#

@app.route('/api/')
def test():
    return 'Hello, world!'


@app.route('/api/words', methods=['POST'])
def main():

    # default keywords
    keywords = ['uh', 'uhm']

    # parse data
    text = request.form.get('text','')
    r_keywords = request.form.get('keywords', None)

    if r_keywords:
        keywords = r_keywords.split(',')
        keywords = [k.strip() for k in keywords]

    # analyze text
    occurances = dict()
    for word in keywords:
        occurances[word] = text.count(word)

    # send back
    return jsonify(occurances)

@app.route('/api/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return  '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data action="/api/upload">
              <p><input type=file name=file>
                 <input type=submit value=Upload>
            </form>
            '''

@app.route('/api/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/api/sensor', methods=['GET', 'POST'])
def sensor():

    global sensorData

    if request.method == 'POST':
        sensorData = None
        sensorData = request.form.copy()
        return 'OK', 200
    else:
        return jsonify(sensorData)
