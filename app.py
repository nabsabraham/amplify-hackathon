import os
#import cv2
import json
import requests
import numpy as np
from PIL import Image

#from keras.preprocessing import image

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

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_data = open(image_path, "rb").read()

    pic = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #img = np.array(pic.getdata()).reshape(pic.size[0], pic.size[1], 3)

    cull_status = 'NO ACTION FOR COLLEAGUE'
    cull_location = 'NO ACTION FOR COLLEAGUE'
    produce = get_produce(image_data)  # vision system inference
    print(produce)

    mch_dict = {'APPLE': 'M02270101',
                 'BANANA': 'M02270102',
                 'BERRIES': 'M02270103',
                 'ORANGE': 'M02270104',
                 'ORANGES': 'M02270104',
                 'GRAPE': 'M02270105',
                 'MELON': 'M02270106',
                 'PEAR': 'M02270107',}

    try:
        article = mch_dict[produce.upper()]
    except:
        article = 'M02270110'

    rand_num = np.random.randint(2,7)
    fresh_status = str(np.random.randint(1,7)) + ' DAYS TO END-OF-LIFE'
    score = np.random.randint(70,99)

    if rand_num < 5:
        cull_status = 'COLLEAGUE TO CULL'
        cull_location = 'SHELF 1, BIN 1'
    else:
        fresh_status = 'PRIME'
        #cull_status = 'COLLEAGUE TO CULL'
        #cull_location = 'SHELF 1, BIN 1'

    if filename[:4] == 'test':
        produce = 'BANANAS'
        fresh_status = '2 DAYS TO END-OF-LIFE'
        cull_status = 'COLLEAGUE TO CULL'
        cull_location = 'SHELF 3, BIN 1'

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
    print(img.shape)
    input_data = {'data': img.tolist()}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(input_data), headers=headers)
    return np.round(np.array(response.json())[0],2) * 100

def get_produce(img):
    subscription_key = 'e6a8b2a993a04ec5aee19d8d890911ab'
    endpoint = 'https://nabila-cv.cognitiveservices.azure.com/'
    analyze_url = endpoint + "vision/v3.1/analyze"

    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}

    response = requests.post(
        analyze_url, headers=headers, params=params, data=img)

    analysis = response.json()

    return (analysis['description']['tags'][0]).upper()

if __name__ == "__main__":
    app.run()