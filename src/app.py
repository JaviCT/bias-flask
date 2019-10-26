#!/usr/bin/python

# Flask
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename
# Keras
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K
# Pandas
import pandas as pd
# Numpy
import numpy as np
# OS
import os
# Config
import config
# Sessions
from uuid import uuid4
# Time
import time


# APP
app = Flask(__name__)
app.secret_key = config.APP_KEY
Bootstrap(app)

# Static path
static_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"))

# Uploads path
uploads_path = os.path.join(static_path, "uploads")
app.config['UPLOAD_FOLDER'] = uploads_path


# LANDING
@app.route('/')
def index():
    return render_template('index.html')


# UPLOAD FILES
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and 'capture' in request.files:
        # File
        f = request.files['capture']
        if f is None or f.filename.strip() == '':
            flash('No file selected!')
        else:
            # Create a unique "session ID" for this particular batch of uploads
            upload_key = str(uuid4())
            # Pattern for file names
            pattern = upload_key + '_' + time.strftime("%Y%m%d-%H%M%S")
            # New filename
            filename = secure_filename(pattern + "_" + f.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Save
            f.save(path)
            print('"{}" saved as "{}"'.format(f.filename, filename))
            # Process
            return redirect(url_for('process', filename=filename))
    # GET
    return render_template('upload.html')


# PROCESS
@app.route("/process/<filename>")
def process(filename):
    # Predict!
    category, prob = 'dog', 1
    path = os.path.join('uploads', filename)
    image = dict(path=path, name=filename, category=category, probability=prob)
    # VIEW
    return render_template('view.html', image=image)


if __name__ == '__main__':
    app.run(host='0.0.0.0')