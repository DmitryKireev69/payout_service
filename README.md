# 1.Клонировать репозиторий:
```
git clone https://github.com/DmitryKireev69/payout_service.git
cd money_collect_service
```
# 2. Создать файл переменных окружения:
```   
В корне проекта есть шаблон:
.env.example
Создайте на его основе рабочий файл .env:
 ```

# 3. Собрать и запустить контейнеры
```
docker compose up -d --build
После выполнения команда поднимет все
необходимые сервисы и создает бд и применяет миграции на неё.
Веб приложение доступно по адресу 127.0.0.1:8000
```

# Полезные команды
```Логи backend:
docker logs -f postgres_db
docker logs -f redis
docker logs -f payout_service
docker logs -f celery_worker
```


# Перезапуск контейнеров из директории с docker-compose.yml:
```
docker compose restart
Остановка проекта:
docker compose down
```