# Utilisation d'une image de base Python légère
FROM python:3.8-slim

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Copie du fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installation des dépendances Python spécifiées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l'intégralité du projet dans le répertoire de travail
COPY . .

# Exposition du port 5000 utilisé par l'application Flask
EXPOSE 5000

# Commande par défaut pour démarrer l'application
CMD ["python", "portfolio.py"]
