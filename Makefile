# Makefile для проекта payout_service

PYTHON=python
MANAGE=$(PYTHON) manage.py
CELERY=celery -A payout_service worker --loglevel=info
TEST_DB=test_payout_db
DB_USER=postgres

# --------------------------------------------------------------------
# Django
# --------------------------------------------------------------------
migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

runserver:
	$(MANAGE) runserver

createsuperuser:
	$(MANAGE) createsuperuser

# --------------------------------------------------------------------
# Тесты
# --------------------------------------------------------------------
# Запуск тестов с автоматической очисткой тестовой базы
test:
	@echo "Очистка тестовой базы $(TEST_DB) перед запуском тестов..."
	psql -U $(DB_USER) -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='$(TEST_DB)';"
	psql -U $(DB_USER) -d postgres -c "DROP DATABASE IF EXISTS $(TEST_DB);"
	@echo "Запуск тестов Django..."
	$(MANAGE) test api.test_payouts --verbosity=2

test-keepdb:
	@echo "Запуск тестов без пересоздания базы"
	$(MANAGE) test api.test_payouts --keepdb --verbosity=2

# --------------------------------------------------------------------
# Celery
# --------------------------------------------------------------------
celery:
	@echo "Запуск Celery воркера"
	$(CELERY)

# --------------------------------------------------------------------
# Очистка тестовой базы вручную
# --------------------------------------------------------------------
drop-test-db:
	@echo "Завершение всех подключений и удаление тестовой базы $(TEST_DB)"
	psql -U $(DB_USER) -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='$(TEST_DB)';"
	psql -U $(DB_USER) -d postgres -c "DROP DATABASE IF EXISTS $(TEST_DB);"

# --------------------------------------------------------------------
# Помощь
# --------------------------------------------------------------------
help:
	@echo "Makefile для payout_service"
	@echo "Доступные команды:"
	@echo "  make migrate          - Применить миграции"
	@echo "  make makemigrations   - Создать миграции"
	@echo "  make runserver        - Запустить сервер Django"
	@echo "  make createsuperuser  - Создать суперпользователя"
	@echo "  make test             - Очистить тестовую БД и запустить тесты"
	@echo "  make test-keepdb      - Запустить тесты без пересоздания базы"
	@echo "  make celery           - Запустить Celery воркера"
	@echo "  make drop-test-db     - Завершить подключения и удалить тестовую базу"
