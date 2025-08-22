version: '3.9'

services:
  web:
    build: .
    container_name: django_web
    command: >
      sh -c "
        python manage.py migrate &&
        python manage.py collectstatic --noinput &&
        daphne -b 0.0.0.0 -p 8047 config.asgi:application
      "
    volumes:
      - .:/app
    ports:
      - "8047:8047"
    depends_on:
      - redis
    environment:
      - DEBUG=1
      - DJANGO_SETTINGS_MODULE=config.settings

  redis:
    image: redis:7
    container_name: redis
    ports:
      - "6379:6379"
