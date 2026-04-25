FROM public.ecr.aws/docker/library/python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# migrations
RUN python manage.py migrate

# static files
RUN python manage.py collectstatic --noinput

EXPOSE 10000

CMD python manage.py migrate && \
python manage.py create_superuser_if_not_exists && \
python manage.py seed_mongo || true && \
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:10000 --workers 2