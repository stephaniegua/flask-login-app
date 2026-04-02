from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from supabase import create_client
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# Connexion Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


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
        nom = request.form["nom"]
        prenom = request.form["prenom"]

        # Vérifier si l'utilisateur existe déjà
        user = supabase.table("users").select("*").eq("mail", mail).execute()

        if user.data:
            return "Utilisateur déjà existant"

        # Ajouter l'utilisateur
        supabase.table("users").insert({
            "nom": nom,
            "prenom": prenom,
            "mail": mail,
            "password": generate_password_hash(password)
        }).execute()

        return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mail = request.form["mail"]
        password = request.form["password"]

        # Chercher l'utilisateur
        user = supabase.table("users").select("*").eq("mail", mail).execute()

        if user.data and check_password_hash(user.data[0]["password"], password):
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

   
