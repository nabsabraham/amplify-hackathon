import os
import json
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

    return render_template('home.html', filename=filename, image_url=image_url,
                           produce='banana')


@app.route("/recommend")
def recommend():
    return render_template('recommender.html')

@app.route("/waste-db")
def waste():
    return render_template('waste.html')


if __name__ == "__main__":
    app.run()