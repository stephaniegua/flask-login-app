from werkzeug.security import generate_password_hash
import mysql.connector

connection = mysql.connector.connect(
    # Créer une connexion à la base MySQL : ouvre un canal de communication avec MySQL permet d’exécuter des requêtes SQL permet de lire et modifier les données
    host='localhost',
    user='root',
    password='',
    database='flasksql'
)
cursor = connection.cursor(dictionary=True)
# Créer un curseur, c’est-à-dire un objet qui permet d’exécuter des requêtes SQL.
# dictionary=True ?Pour que les résultats soient retournés sous forme de dictionnaire : C’est plus pratique que des tuples.

cursor.execute("SELECT id, password FROM users")
# Exécuter une requête SQL.Cela récupère tous les utilisateurs.
users = cursor.fetchall()
#Récupérer toutes les lignes retournées par la requête.

for user in users:
    #Boucle for user in users:Parcourir chaque utilisateur pour : lire son mot de passe en clair
#le hacher, mettre à jour la base
    hashed = generate_password_hash(user["password"])
    #Fonction fournie par Werkzeug, utilisée par Flask.Rôle : Transformer un mot de passe en clair en une chaîne hachée non réversible.
    cursor.execute(
        #Mettre à jour la base avec le mot de passe haché
        "UPDATE users SET password = %s WHERE id = %s",
        (hashed, user["id"])
    )

connection.commit()
#Valider les modifications dans la base.Sans commit(), rien n’est enregistré.
cursor.close()
connection.close()
#Fermer proprement :le curseur, la connexion MySQL C’est important pour éviter :les fuites de mémoire les connexions ouvertes inutiles

print("Migration terminée : tous les mots de passe sont maintenant hachés.")
#Juste un message pour confirmer que tout s’est bien passé.