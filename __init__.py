from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
#test#                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str
  
@app.route('/decrypt/<string:token_chiffre>')
def decryptage(token_chiffre):
    token_bytes = token_chiffre.encode() # Conversion str -> bytes
    try:
        valeur_dechiffree_bytes = f.decrypt(token_bytes) # Déchiffre le token
        valeur_dechiffree_str = valeur_dechiffree_bytes.decode() # Conversion bytes -> str
        return f"Valeur déchiffrée : {valeur_dechiffree_str}"
    except Exception as e:
        # Gère les erreurs potentielles de déchiffrement (ex: token invalide, mauvaise clé)
        return f"Erreur de déchiffrement : {str(e)}. Assurez-vous que le token est correct et que la clé utilisée pour le chiffrement est la même."
                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)
