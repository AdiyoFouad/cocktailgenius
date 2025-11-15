# Dockerfile pour Flask avec Python 3.11
FROM python:3.11-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copier requirements et installer les dépendances
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . .

# Exposer le port (Render l'utilise)
EXPOSE 5000

# Variables d'environnement par défaut (peut être surchargé sur Render)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PORT=5000

# Lancer l'application avec Gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
CMD ["sh", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:5000 app:app"]
