#!/bin/sh

echo "Ожидание запуска базы данных..."
while ! nc -z db 5432; do
  sleep 1
done
echo "База данных готова!"

if [ "$1" = "django" ]; then
    echo "Применение миграций..."
    python manage.py migrate --noinput
    echo "Запуск сервера Django..."
    exec python manage.py runserver 0.0.0.0:8000

elif [ "$1" = "celery" ]; then
    shift
    echo "Запуск Celery воркера..."
    exec celery -A collect_service worker "$@"

else
    echo "Неизвестная команда, выполнение: $@"
    exec "$@"
fi