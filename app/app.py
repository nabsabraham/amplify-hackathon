from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

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
    return render_template("upload.html", name='Nabila')

    #if request.method == "POST":
        #req = request.form
        #print(req)
        #return redirect(request.url)

    #return render_template("upload.html")



    return render_template("public/upload_image.html")
if __name__ == "__main__":
    app.run()