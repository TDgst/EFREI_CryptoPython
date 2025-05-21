from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template_string, render_template, jsonify
from flask import request # Ajouté pour potentiellement lire des query parameters plus tard si besoin

# Imports non utilisés dans le code actuel, conservés de l'original :
# from flask import json
# from urllib.request import urlopen
# import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Assurez-vous d'avoir un fichier 'hello.html' dans un dossier 'templates'
    # ou remplacez par une simple chaîne de caractères ou render_template_string
    try:
        return render_template('hello.html')
    except:
        return "Bienvenue ! Utilisez /encrypt/votre_cle/votre_valeur ou /decrypt/votre_cle/votre_token"

# La génération globale de clé n'est plus nécessaire ici,
# car la clé sera fournie dans chaque requête.
# key = Fernet.generate_key()
# f = Fernet(key)

@app.route('/generate_key')
def generate_new_key():
    """Route optionnelle pour aider l'utilisateur à générer une clé valide."""
    new_key = Fernet.generate_key()
    return f"Voici une clé Fernet que vous pouvez utiliser : {new_key.decode()}"

@app.route('/encrypt/<string:user_key_str>/<string:valeur>')
def encryptage(user_key_str, valeur):
    try:
        # Convertir la clé fournie par l'utilisateur (str) en bytes
        user_key_bytes = user_key_str.encode()
        f = Fernet(user_key_bytes)
    except Exception as e:
        return f"Erreur : La clé fournie n'est pas valide. Une clé Fernet est une chaîne encodée en Base64 URL-safe. Erreur détaillée : {str(e)}"

    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    try:
        token = f.encrypt(valeur_bytes)  # Chiffre la valeur
        return f"Valeur chiffrée : {token.decode()}"  # Retourne le token en str
    except Exception as e:
        return f"Erreur lors du chiffrement : {str(e)}"

@app.route('/decrypt/<string:user_key_str>/<string:token_chiffre>')
def decryptage(user_key_str, token_chiffre):
    try:
        # Convertir la clé fournie par l'utilisateur (str) en bytes
        user_key_bytes = user_key_str.encode()
        f = Fernet(user_key_bytes)
    except Exception as e:
        return f"Erreur : La clé fournie n'est pas valide. Une clé Fernet est une chaîne encodée en Base64 URL-safe. Erreur détaillée : {str(e)}"

    token_bytes = token_chiffre.encode() # Conversion str -> bytes
    try:
        valeur_dechiffree_bytes = f.decrypt(token_bytes) # Déchiffre le token
        valeur_dechiffree_str = valeur_dechiffree_bytes.decode() # Conversion bytes -> str
        return f"Valeur déchiffrée : {valeur_dechiffree_str}"
    except InvalidToken:
        return "Erreur de déchiffrement : Token invalide. Cela peut être dû à un token incorrect, corrompu ou une mauvaise clé."
    except Exception as e:
        # Gère les autres erreurs potentielles de déchiffrement
        return f"Erreur de déchiffrement : {str(e)}. Assurez-vous que le token est correct et que la clé utilisée pour le chiffrement est la même."

if __name__ == "__main__":
  app.run(debug=True)
