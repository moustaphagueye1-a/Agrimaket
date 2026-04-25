FROM public.ecr.aws/docker/library/python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 10000

# Lance les migrations PUIS démarre gunicorn
CMD python manage.py migrate && gunicorn ecommerce.wsgi --bind 0.0.0.0:10000 --workers 2