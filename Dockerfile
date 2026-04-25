FROM public.ecr.aws/docker/library/python:3.11-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dossier de travail
WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copier requirements
COPY requirements.txt /app/

# Installer dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . /app/

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port
EXPOSE 10000
# Commande de lancement
CMD python manage.py migrate && \
python manage.py seed_mongo || true && \
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:10000 --workers 2