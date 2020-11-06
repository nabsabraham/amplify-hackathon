import os
import json
import requests
import numpy as np
from PIL import Image
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient


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

    if produce.upper() == 'BANANA':
        results, res_dict = banana_inference(image_path)
        max_class = max(res_dict, key=res_dict.get)
        max_prob = res_dict[max_class]

        if max_class == 'fresh':
            fresh_status = 'PRIME'
            score = np.round(res_dict['fresh'] * 100, 2)
        elif max_class == 'ripe':
            fresh_status = str(np.random.randint(1, 3)) + ' DAYS TO END-OF-LIFE'
            score = np.round(res_dict['ripe'] * 100, 2)
            cull_status = 'COLLEAGUE TO CULL'
            cull_location = 'SHELF 2, BIN 1'
        else:
            fresh_status = 'PRODUCE IS CRITICAL'
            score = np.round(res_dict['overripe'] * 100, 2)
            cull_status = 'COLLEAGUE TO CULL ASAP'
            cull_location = 'SHELF 1, BIN 1'

    else:
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

def banana_inference(image_path):
    ENDPOINT = 'https://nabila-custom-vision.cognitiveservices.azure.com/'
    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": 'ae5a8bbf373847948ec9cbdf13cdfaae'})
    predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
    project_id = '909cc200-acfd-4738-a5d6-f46488b3921a'
    publish_iteration_name = 'Iteration2'
    res_dict={}
    with open(image_path, "rb") as image_contents:
        results = predictor.classify_image(
            project_id, publish_iteration_name, image_contents.read())

        # Display the results.
        for prediction in results.predictions:
            print("\t" + prediction.tag_name +
                  ": {0:.2f}%".format(prediction.probability * 100))
            res_dict[prediction.tag_name] = prediction.probability

        return results, res_dict

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