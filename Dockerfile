# 1. Utiliser une image Python officielle
FROM public.ecr.aws/docker/library/python:3.11-slim

# 2. Définir des variables d'environnement pour éviter les fichiers .pyc et bufferiser les logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Définir le répertoire de travail dans le conteneur
WORKDIR /app

# 4. Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# 5. Installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copier le reste du projet
COPY . /app/

# 7. Exposer le port par défaut de Django
EXPOSE 8000

# 8. Commande pour lancer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]