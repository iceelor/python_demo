import json
import os
from werkzeug.utils import secure_filename
from DataBaseTool import DataBaseTool, ModelInfo, ModelImage
from TaobaoMM import get_data

__author__ = 'www.showbt.com'

# -*- encoding: UTF-8 -*-

from sqlalchemy import func
from flask import Flask, request, render_template, redirect, url_for

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        f = request.files['myfile']
        if f:
            f.save('/data/' + secure_filename(f.filename))
        return redirect(url_for("index_html", name=name))
    else:
        return render_template("login.html")


@app.route("/")
@app.route("/taomm", methods=['GET'])
def index_html():
    db = DataBaseTool()
    session = db.get_session()
    p = request.args.get('page', 1)
    page_size = 10
    try:
        total_record = session.query(func.count('*')).select_from(ModelInfo)
        current_page = set_page(int(p), page_size, total_record[0][0])
        query = session.query(ModelInfo).offset((current_page - 1) * page_size).limit(page_size)
    finally:
        db.close_session(session)
    t = request.args.get('type')
    if t == 'json':
        ja = []
        for mi in query:
            ja.append(mi.to_json())
        return json.dumps(ja)
    return render_template("index.html", name=query, page=current_page)


def set_page(current_page, page_size, total_record):
    if current_page < 1:
        current_page = 1
    if total_record % page_size != 0:
        max_page = total_record / page_size + 1
    else:
        max_page = total_record / page_size
    if current_page > max_page:
        current_page = max_page
    return current_page


@app.route('/taomm/<id>')
def detail_img(id=None):
    db = DataBaseTool()
    session = db.get_session()
    query = session.query(ModelImage).filter(ModelImage.miid == id)
    return render_template("detail_img.html", images=query)


@app.route('/getdata')
def init_data():
    start = request.args.get('start', 1)
    end = request.args.get('end', 10)
    get_data(int(start), int(end))
    return 'finish'


if __name__ == '__main__':
    app.debug = True
    app.run()
