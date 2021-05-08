# import flask
# from flask import request, jsonify

# app = flask.Flask(__name__)
# app.config["DEBUG"] = True

# # Create some test data for our catalog in the form of a list of dictionaries.
# books = [
#     {'id': 0,
#      'title': 'A Fire Upon the Deep',
#      'author': 'Vernor Vinge',
#      'first_sentence': 'The coldsleep itself was dreamless.',
#      'year_published': '1992'},
#     {'id': 1,
#      'title': 'The Ones Who Walk Away From Omelas',
#      'author': 'Ursula K. Le Guin',
#      'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
#      'published': '1973'},
#     {'id': 2,
#      'title': 'Dhalgren',
#      'author': 'Samuel R. Delany',
#      'first_sentence': 'to wound the autumnal city.',
#      'published': '1975'}
# ]


# @app.route('/', methods=['GET'])
# def home():
#     return '''<h1>Distant Reading Archive</h1>
# <p>A prototype API for distant reading of science fiction novels.</p>'''


# # A route to return all of the available entries in our catalog.
# @app.route('/api/v1/resources/books/all', methods=['GET'])
# def api_all():
#     return jsonify(books)

# app.run()
import create_v_bg
import json
import base64
import os

from flask import Flask, flash, request, redirect, url_for
# from flask import send_file
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


IMG_NAME = "img"
BG_NAME = "bg"
IMG_FILE = ""
BG_FILE = ""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


def set_name(filename, is_bg=False):
    _, ext = os.path.splitext(filename)
    if is_bg:
        global BG_FILE
        BG_FILE = BG_NAME+ext
        return "{name}{ext}".format(name=BG_NAME, ext=ext)
    else:
        global IMG_FILE
        IMG_FILE = IMG_NAME+ext
        return "{name}{ext}".format(name=IMG_NAME, ext=ext)


@app.route('/', methods=['GET'])
def dynamic_page():
    file_name = create_v_bg.create_v_bg(IMG_FILE, BG_FILE)
    data = {}
    with open(file_name, mode='rb') as file:
        img = file.read()
    data['img'] = base64.encodebytes(img).decode('utf-8')
    # os.remove(IMG_FILE)
    # os.remove(BG_FILE)
    return json.dumps(data)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload-img', methods=['POST'])
def upload_img():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = set_name(filename, False)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename))
    
@app.route('/upload-bg', methods=['POST'])
def upload_bg():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = set_name(filename, True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file',
                                filename=filename))


if __name__ == '__main__':
    app.run(debug=True)
