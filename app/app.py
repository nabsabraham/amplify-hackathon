import os
import cv2
import json
import requests
import numpy as np
from keras.preprocessing import image

from werkzeug.utils import secure_filename
from flask import Flask, render_template, url_for, request, redirect, abort

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(path)
    image_url = url_for('static', filename='uploads/'+str(filename))
    img = image.load_img(os.path.join(app.config['UPLOAD_FOLDER'], filename), (300,300))

    cull_status = 'N/A'
    cull_location = 'N/A'
    score = 100

    if filename[3] == 'O':
        produce = 'ORANGE'
        article = 'MCH033'
    elif filename[3] == 'B':
        produce = 'BANANA'
        article = 'MCH034'
    else:
        produce = 'APPLE'
        article = 'MCH013'

    if filename[0:4] == 'MDLO':
        fresh_status = '6 DAYS TO END-OF-LIFE'
    elif filename[0:4] == 'MDLB':
        fresh_status = '3 DAYS TO END-OF-LIFE'
    elif filename[0:4] == 'MDLA':
        fresh_status = '7 DAYS TO END-OF-LIFE'
    else:
        img = np.array(img)
        score = inference(img)
        fresh_status = 'SPOILED' if score > 80 else 'PRIME'
        cull_status = 'COLLEAGUE TO CULL' if score > 80 else "N/A"
        cull_location = 'SHELF 3, BIN 2' if cull_status != 'N/A' else "N/A"

    return render_template('home.html', filename=filename, image_url=image_url,
                           produce=produce, article=article, score=(str(score) + '%'),
                           fresh_status=fresh_status, cull_status=cull_status, cull_location=cull_location)

@app.route("/recommend")
def recommend():
    return render_template('recommender.html')

@app.route("/waste-db")
def waste():
    return render_template('waste.html')

def inference(img):
    url = 'http://b790f0dc-11c1-41fb-8ccd-7f1f67567d49.westus.azurecontainer.io/score'
    input_data = {'data': img.tolist()}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(input_data), headers=headers)
    return np.round(np.array(response.json())[0],2) * 100

if __name__ == "__main__":
    app.run()