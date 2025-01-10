from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", titolo="Home")

@app.route("/register")
def register():
    return render_template("register.html", titolo="Register")

@app.route("/login")
def login():
    return render_template("login.html", titolo="Login")

app.run()
