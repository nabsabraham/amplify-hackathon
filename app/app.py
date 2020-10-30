import os
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
    return render_template('home.html', filename=filename, image_url=image_url)

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
        if 'image_file' not in request.files:
            return 'there is no image_file in form!'
        image_file = request.files['image_file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(path)
        return render_template('form.html', path=path, filename=image_file)

@app.route('/display/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route("/recommend")
def recommend():
    return render_template('recommender.html')


if __name__ == "__main__":
    app.run()