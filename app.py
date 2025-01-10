from flask import Flask, render_template
from flask_mysqldb import MySQL

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

@app.route("/personale")
def personale():
    return render_template("personale.html", titolo="Personale")

if __name__ == '__main__': 
    app.run(debug=True)
