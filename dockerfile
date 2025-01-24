# Utiliser une image de base Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier Pipfile et Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Installer pipenv et les dépendances du projet
RUN pip install pipenv && pipenv install --system --deploy

# Copier tout le reste du projet
COPY . .

# Commande par défaut
CMD ["flask", "run"]
