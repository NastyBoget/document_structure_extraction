import os
from typing import List, Dict

from flask import Flask, request
import tempfile

from pdf2text import pdf2text
import pickle as pkl
from werkzeug.datastructures import FileStorage
from string2features import string2features, AddFeatures
import json

static_path = os.path.join(os.path.dirname(__file__))
app = Flask(__name__, static_url_path=static_path)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

types = {1: "header", 2: "list", 3: "text"}

def doc2json(path: str) -> List[Dict]:
    X = pdf2text(path)
    clf = pkl.load(open("model.pkl", "rb"))
    y = clf.predict(X)
    res = []
    for line, type_ in zip(X, y):
        res.append({"type": types[int(type_)], "content": line})
    return res


def _get_file(request) -> FileStorage:
    return request.files['file']

def process_file_and_send_response(path):
    json_string = doc2json(path)

    response = app.response_class(
        response=json.dumps(obj=json_string, ensure_ascii=False, indent=2),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        uploaded_file = _get_file(request)
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp_path = os.path.join(tmpdirname, uploaded_file.filename.split("/")[-1])
            uploaded_file.save(tmp_path)
            return process_file_and_send_response(tmp_path)

    return app.send_static_file("main_page.html")


@app.route('/example_pdf', methods=['GET'])
def send_pdf():
    path = "example.pdf"
    return app.send_static_file(path)


@app.route("/example_json", methods=['GET'])
def process_pdf():
    return process_file_and_send_response("static/example.pdf")


if __name__ == "__main__":
    # app.secret_key = b'_5#y2L_h4Q8z\n\xec]/'
    app.run(host='0.0.0.0', port=8888)
