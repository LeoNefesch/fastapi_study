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
или...
```commandline
alembic upgrade head
```

### Решение проблем с миграциями:
Если в БД ещё нет данных, а при обновлении струкутры БД возникли ошибки, то вы можете вручеую удалить файлы .py из
migrations/versions и SQL-запросами удалить созданные таблицы, например:
```commandline
DROP TABLE roles;
```
```commandline
DROP TABLE users;
```
```commandline
DROP TABLE alembic_version;
```
А затем 
```commandline
alembic revision --autogenerate -m "Initial db"
```
и
```commandline
alembic upgrade head
```