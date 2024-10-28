# FastAPI
## Миграции
Самые первые команды (для создания миграций)
```commandline
alembic init migrations
```
```commandline
alembic revision --autogenerate -m "Database creation"
```
Создание таблиц в БД (применение миграций)
```commandline
alembic upgrade <migrations.versions.....py.revision>
```
