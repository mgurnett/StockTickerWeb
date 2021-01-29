from flask import Flask, render_template, request

import datetime
from db_data import *
from ST_classes_NEW import *

app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get("name", "Michael") #Michael is the default
    title = "INDEX"
    return render_template ("index.html", title = title, name = name)

@app.route('/about')
def about():
    title = "ABOUT"
    return render_template ("about.html", title = title) 