FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app

WORKDIR $APP_HOME

# system deps for mysqlclient or pymysql (choose one; this is mysqlclient)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential default-libmysqlclient-dev pkg-config curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt gunicorn

# copy project
COPY . .

# collect static (safe even if no static files yet)
RUN mkdir -p /static && python manage.py collectstatic --noinput || true

# create a tiny health endpoint if you don’t have one:
# (Django will 404 on /health by default; that’s fine for liveness if we use TCP check)
# Better: add a /health view later and switch probes to HTTP.

EXPOSE 8000

# Gunicorn
CMD ["gunicorn", "therapist_webapi.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60"]
