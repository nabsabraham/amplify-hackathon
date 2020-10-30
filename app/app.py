import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

UPLOADS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static\\images')

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/recommend")
def recommend():
    return render_template('recommender.html')

@app.route("/upload")
def upload():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            print(image)
            #return redirect(request.url)
    return render_template("upload.html")

# we are posting to this page from the /home page
@app.route("/form", methods=['POST'])
def form():
    if request.method == 'POST':
        image_name = request.form['filename']
        if image_name != '':
            path = os.path.join(UPLOADS_PATH, secure_filename(image_name))
            #image_name.save(path)
        return render_template('form.html', image_name=image_name, path=path)
    #if request.method == "POST":
        #req = request.form
        #print(req)
        #return redirect(request.url)

    #return render_template("upload.html")



if __name__ == "__main__":
    app.run()