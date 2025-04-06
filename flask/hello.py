from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello, World<h1>"

@app.route("/home")
def home():
    return "<h1>Home page<h1>"

@app.route("/about")
def about():
    return "<h1>About Page<h1>"


if __name__=="__main__":
    app.run(debug=True)