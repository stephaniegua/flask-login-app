from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:qomNudGnKknSRUOtDsVOMclmIXAuyYRR@caboose.proxy.rlwy.net:40805/railway"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


@app.route("/")
def home():
    if "user" in session:
        return render_template("home.html", user=session["user"])
    return render_template("home.html", user=None)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        mail = request.form["mail"]
        password = request.form["password"]

        # Vérifier si l'utilisateur existe déjà dans Railway 
        user = User.query.filter_by(mail=mail).first() 
        if user:
            return "Utilisateur déjà existant"
        
        # Ajouter l'utilisateur dans Railway 
        new_user = User( 
                        mail=mail, 
                        password=generate_password_hash(password) 
                        )
        db.session.add(new_user)
        db.session.commit()
        
        return redirect("/login")
    
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mail = request.form["mail"]
        password = request.form["password"]

        # Chercher l'utilisateur dans Railway
        user = User.query.filter_by(mail=mail).first()

        if user and check_password_hash(user.password, password):
            session["user"] = mail
            return redirect("/")

        return "Identifiants incorrects"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
