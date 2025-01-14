from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "138.41.20.102"
app.config["MYSQL_PORT"] = 53306
app.config["MYSQL_USER"] = "ospite"
app.config["MYSQL_PASSWORD"] = "ospite"
app.config["MYSQL_DB"] = "w3schools"

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("home.html", titolo="Home")

@app.route("/registrati", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", titolo="Register")
    else:
        nome = request.form.get("nome") #il nome nella parentesi si riferisce al nome nel campo name dell'input del form
        cognome = request.form.get("cognome")
        username = request.form.get("username")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")

        if nome == "" or cognome == "" or username == "" or password == "" or cpassword == "":  #se almeno uno dei campi è vuoto non metti nel database e ritorni errore
            return render_template("register.html", errore="Campo non valido")
        else:
            if password != cpassword:
                return render_template("register.html", errore="Campi password diversi") #i campi sono stati tutti inseriti ma le password non coincidono
            else:
                cursor = mysql.connection.cursor()

                select = "SELECT * FROM users WHERE username=%s "
                
                #devo controllare lo username
                if cursor.execute(select(username,)) 

                insert = "INSERT INTO users VALUES(%s, %s, %s, %s)"

                cursor.execute(insert, (nome, cognome, username, password)) #il cpassword serve solo per il controllo e non va inserito nel database

                mysql.connection.commit() #per fare il commit

                cursor.close()

                return redirect(url_for('home'))
                #return redirect("/inserisci la route e non il nome della funzione")

@app.route("/login")
def login():
    return render_template("login.html", titolo="Login")

@app.route("/personale")
def personale():
    return render_template("personale.html", titolo="Personale")



if __name__ == '__main__': 
    app.run(debug=True)
