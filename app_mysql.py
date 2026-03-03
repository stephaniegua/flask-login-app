from flask import Flask, request, render_template
import mysql.connector
from flask import redirect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Liste des utilisateurs connectés
users_connected = []

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='flasksql'
    )
    
class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='flasksql'
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def get_user(self, email,):
        self.cursor.execute(
            "SELECT * FROM users WHERE mail = %s",
            (email,)
        )
        return self.cursor.fetchone()

    def insert_user(self, email, hashed_password):
        self.cursor.execute(
            "INSERT INTO users (mail, password) VALUES (%s, %s)",
            (email, hashed_password)
        )
        self.connection.commit()
    

@app.context_processor#C'est un décorateur Flask qui permet d'injecter des variables dans tous les templates.
def inject_user():#C’est le nom de la fonction que je donne au context processor.
    return {#Je retourne  obligatoirement  un dictionnaire Python.
        "user_connected": bool(users_connected),
        "user": users_connected[0] if users_connected else None
    }

@app.route("/")
def home():
    if users_connected:
        return render_template(
            "home.html", 
            title="Accueil", )
    else:
        return render_template(
            "home.html", 
            title="Accueil", 
            user=None)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = Database() 
        user = db.get_user(email,) 
        if user and check_password_hash(user["password"], password): 
            users_connected.clear() 
            users_connected.append(email) 
            return render_template(
                "login.html", 
                success=True, 
                user=email,
                message="Connexion réussie !"
                ) 
        else: 
            return render_template(
                "login.html", 
                success=False, 
                message="Identifiants incorrects.") 
    return render_template(
        "login.html")

@app.route("/logout") 
def logout(): 
    users_connected.clear() 
    return redirect("/")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        # Vérifications
        if "@" not in email:
            return render_template(
                "signup.html", 
                success=False,
                message="Email invalide."
                )

        if password != confirm:
            return render_template(
                "signup.html", 
                success=False,
                message="Les mots de passe ne correspondent pas."
                )

        db = Database() 
        hashed_password = generate_password_hash(password)
        db.insert_user(email, hashed_password) 
        return render_template(
            "signup.html", 
            success=True, 
            message="Inscription réussie !"
            ) 
    return render_template(
        "signup.html"
        )

if __name__ == "__main__":
    app.run(debug=True)

        