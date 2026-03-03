from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret-key"

# Remplace la base MySQL par une liste Python
users = []  # Exemple : {"mail": "test@test.com", "password": "hash"}

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

        # Vérifier si l'utilisateur existe déjà
        for u in users:
            if u["mail"] == mail:
                return "Utilisateur déjà existant"

        # Ajouter l'utilisateur
        users.append({
            "mail": mail,
            "password": generate_password_hash(password)
        })

        return redirect("/login")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mail = request.form["mail"]
        password = request.form["password"]

        # Vérifier l'utilisateur
        for u in users:
            if u["mail"] == mail and check_password_hash(u["password"], password):
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
