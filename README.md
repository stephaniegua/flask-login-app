# flask-login-app
Création d'une application flask
Application web simple de gestion d’utilisateurs (inscription / connexion) développée avec **Flask** et une base de données **PostgreSQL via Supabase**.

---

## 🚀 Fonctionnalités

* 📝 Inscription utilisateur (signup)
* 🔑 Connexion sécurisée (login)
* 🔒 Hashage des mots de passe
* 👤 Gestion de session utilisateur
* 🗄️ Stockage des données avec Supabase (PostgreSQL)
* 🌐 Déploiement en ligne avec Render

---

## 🛠️ Technologies utilisées

* **Python / Flask**
* **Werkzeug** (hash des mots de passe)
* **Supabase** (PostgreSQL)
* **Gunicorn** (serveur de production)
* **Render** (hébergement)

---

## 📂 Structure du projet

```
.
├── app.py
├── requirements.txt
├── templates/
│   ├── partials/
│   │   ├── head.html
│   │   ├── body.html
│   │   └── footer.html
│   ├── home.html
    ├── base.html
│   ├── login.html
│   └── signup.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── img//
           └── background.png
```

---

## ⚙️ Installation en local

### 1. Cloner le projet

```bash
git clone https://github.com/stephaniegua/flask-login-app.git
cd flask-login-app
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration

Créer des variables d’environnement :

```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_anon_key
SECRET_KEY=your_secret_key
```

---

## ▶️ Lancer l’application

```bash
python app.py
```

Puis ouvrir :

```
http://127.0.0.1:5000
```

---

## 🌐 Déploiement

L’application est déployée avec **Render** :

* Build command :

```
pip install -r requirements.txt
```

* Start command :

```
gunicorn app:app
```

---

## 🗄️ Base de données

L’application utilise **Supabase (PostgreSQL)** pour stocker les utilisateurs.

- Table : `users`
- Hébergement de la base en ligne
- Accès via API avec clé sécurisée

Table `users` :

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  nom VARCHAR(255) NOT NULL,
  prenom VARCHAR(255) NOT NULL,
  mail VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
);
```

---

## ⚠️ Problèmes rencontrés et solutions

### ❌ Clé Supabase invalide

➡️ Utiliser la **anon public key** (et pas la publishable key)

---

### ❌ Conflit de dépendances (`httpx`)

➡️ Fixer les versions dans `requirements.txt`

---

### ❌ Erreur `NOT NULL`

➡️ Ajouter `nom` et `prenom` dans le formulaire signup

---

### ❌ Erreur `duplicate key`

➡️ Réinitialiser la séquence PostgreSQL :

```sql
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
```

---

## 🔒 Sécurité

* Mots de passe hashés avec `werkzeug.security`
* Sessions Flask protégées par `SECRET_KEY`

---

## 📌 Améliorations possibles

* Validation des formulaires
* Messages d’erreur utilisateur (flash)
* Interface utilisateur améliorée
* Authentification avancée (JWT, OAuth)

---

## 👩‍💻 Auteur

Projet réalisé dans le cadre d’un apprentissage Flask / déploiement web.

---

## 📄 Licence

Projet libre d’utilisation à des fins pédagogiques.
