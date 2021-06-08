from application import app
from flask import render_template


@app.route("/")
def home():
    return render_template("index.html", home=True)


@app.route("/register")
def register():
    return render_template("register.html", register=True)


@app.route("/login")
def login():
    return render_template("login.html", login=True)
