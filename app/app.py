from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/upload")
def sign_up():
    if request.method == "POST":

        req = request.form
        print(req)

        return redirect(request.url)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run()