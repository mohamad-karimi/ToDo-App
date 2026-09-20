FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements-docker.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements-docker.txt

COPY . .

WORKDIR /app/core

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["sh", "-c", "gunicorn core.wsgi --bind 0.0.0.0:${PORT:-8000}"]