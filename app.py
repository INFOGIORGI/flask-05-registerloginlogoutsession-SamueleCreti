from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash #per gestire l'hash

app = Flask(__name__)
app.secret_key = 'una-chiave-segreta' #affinchè la flash funzioni bisogna avere una chiave segreta. I dati vengono passati nei cookie e cifrati

app.config["MYSQL_HOST"] = "138.41.20.102"
app.config["MYSQL_PORT"] = 53306
app.config["MYSQL_USER"] = "ospite"
app.config["MYSQL_PASSWORD"] = "ospite"
app.config["MYSQL_DB"] = "w3schools"

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("home.html", titolo="Home")

@app.route("/registrati", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", titolo="Register")
    
    nome = request.form.get("nome", "") #il nome nella parentesi si riferisce al nome nel campo name dell'input del form
    cognome = request.form.get("cognome", "")# se la chiave cognome non viene trovata nella richiesta HTTP viene assegnato il valore "" (altrimenti verrebbe assegnato None)
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    cpassword = request.form.get("cpassword", "")

    if nome == "" or cognome == "" or username == "" or password == "" or cpassword == "":  #se almeno uno dei campi è vuoto non metti nel database e ritorni errore
        flash("Campo non valorizzato")
        return redirect(url_for('register'))
    else:
        if password != cpassword:
            flash("Campi password diversi")
            return redirect(url_for('register')) #i campi sono stati tutti inseriti ma le password non coincidono
        
        cursor = mysql.connection.cursor()
        
        #Prima query: devo controllare lo username
        select = "SELECT username FROM users WHERE username = %s"
        cursor.execute(select, (username,))
        dati = cursor.fetchall()

        if len(dati) != 0: #se la tupla di tuple non è vuota (lunghezza 0) vuol dire che lo username è già presente nel db
            flash("Username già esistente")
            return redirect(url_for('register'))

        #seconda query: eseguo la registrazione inserendo i campi del form nel db
        insert = "INSERT INTO users VALUES(%s, %s, %s, %s)"
        hashPassword = generate_password_hash(password) #devo mascherare tramite hash la password
        cursor.execute(insert, (username, hashPassword, nome, cognome)) #il cpassword serve solo per il controllo e non va inserito nel database
        mysql.connection.commit() #per fare il commit

        cursor.close()

        return redirect(url_for('home'))
        #return redirect("/inserisci la route e non il nome della funzione")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", titolo="Login")
    
    username = request.form.get("username")
    password = request.form.get("password")

    cursor = mysql.connection.cursor()

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    dati = cursor.fetchall()

    if len(dati) == 0:
        flash("Dati errati")
        return redirect(url_for('login'))
    
    cursor.close()

    return redirect(url_for('personale'))

    

@app.route("/personale")
def personale():
    return render_template("personale.html", titolo="Personale")

if __name__ == '__main__': 
    app.run(debug=True)
