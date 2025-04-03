#!/usr/bin/env python3
# Importation des modules nécessaires
from flask import Flask, render_template_string
import mysql.connector
import os

app = Flask(__name__)

# Récupération des variables d'environnement pour la connexion à la base de données
DB_HOST = os.environ.get('DB_HOST', 'localhost')          # Adresse de la base de données (sera remplacée par le nom du service Kubernetes)
DB_USER = os.environ.get('DB_USER', 'portfolio_user')       # Utilisateur MySQL
DB_PASS = os.environ.get('DB_PASS', 'portfolio_pass')       # Mot de passe MySQL
DB_NAME = os.environ.get('DB_NAME', 'portfolio_db')         # Nom de la base de données
RESET_DB = os.environ.get('RESET_DB', 'false').lower() == 'true'  # Option de réinitialisation de la base (true ou false)

def get_db_connection():
    """
    Fonction pour établir une connexion à la base de données MySQL
    """
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    return conn

def init_db():
    """
    Fonction pour initialiser la base de données :
    - Crée la base de données si elle n'existe pas.
    - Réinitialise la table 'visits' si RESET_DB est activé.
    - Crée la table 'visits' pour stocker le nombre de visites.
    - Insère une valeur initiale (0) si la table est vide.
    """
    # Connexion sans préciser la base pour créer la base si nécessaire
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.commit()
    conn.close()
    
    # Connexion à la base de données créée
    conn = get_db_connection()
    cursor = conn.cursor()
    if RESET_DB:
        # Si la variable RESET_DB est true, on supprime la table existante pour réinitialiser le compteur
        cursor.execute("DROP TABLE IF EXISTS visits")
        conn.commit()
    # Création de la table 'visits' si elle n'existe pas
    cursor.execute("CREATE TABLE IF NOT EXISTS visits (count INT)")
    conn.commit()
    # Si la table est vide, insertion d'une ligne initiale avec 0 visite
    cursor.execute("SELECT * FROM visits")
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO visits (count) VALUES (0)")
        conn.commit()
    conn.close()

@app.route('/')
def index():
    """
    Route principale de l'application :
    - Récupère le nombre actuel de visites.
    - Incrémente le compteur.
    - Affiche le portfolio avec le nombre de visites.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM visits")
    result = cursor.fetchone()
    visits = result[0] if result else 0

    # Incrémenter le nombre de visites de 1
    new_visits = visits + 1
    cursor.execute("UPDATE visits SET count = %s", (new_visits,))
    conn.commit()
    conn.close()
    
    # Code HTML de la page affichée
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Portfolio DevOps - Georges Momo</title>
        <style>
            /* Styles CSS pour un rendu moderne et captivant */
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .header {{
                background-color: #333;
                color: #fff;
                padding: 20px;
                text-align: center;
            }}
            .content {{
                padding: 20px;
            }}
            .section {{
                margin-bottom: 20px;
            }}
            .card {{
                background-color: #fff;
                padding: 20px;
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Georges Momo - Ingénieur Java - DevOps</h1>
            <p>9 ans d'expérience - Expert en déploiement, CI/CD, Cloud et automatisation</p>
        </div>
        <div class="content">
            <div class="section">
                <h2>Projets</h2>
                <div class="card">
                    <h3>Projet 1: Infrastructure as Code</h3>
                    <p>Mise en place d'environnements automatisés avec Ansible et Terraform.</p>
                </div>
                <div class="card">
                    <h3>Projet 2: CI/CD avec Jenkins</h3>
                    <p>Automatisation des déploiements avec Jenkins, Docker et Kubernetes.</p>
                </div>
                <div class="card">
                    <h3>Projet 3: Monitoring et Log Management</h3>
                    <p>Implémentation de solutions de monitoring avec Prometheus et Grafana.</p>
                </div>
            </div>
            <div class="section">
                <h2>Compétences</h2>
                <p>Compétences en développement Java, scripts Bash, gestion des conteneurs, cloud computing et bien plus...</p>
            </div>
            <div class="section">
                <h2>Nombre de visites</h2>
                <p>Nombre de visites sur ce portfolio : <strong>{new_visits}</strong></p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    # Initialisation de la base de données avant le lancement de l'application
    init_db()
    # Démarrage de l'application Flask sur toutes les interfaces (0.0.0.0) et sur le port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
