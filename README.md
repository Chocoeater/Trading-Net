# TradingNet
Веб-приложение для управления сетью поставщиков и продуктов. Реализовано на Django с использованием DRF и PostgreSQL. Поддерживает API с фильтрацией, поиском и ограничениями доступа для сотрудников.

---

## Стек технологий

- Python 3.13  
- Django 5.x  
- Django REST Framework  
- PostgreSQL  
- Docker / Docker Compose  
- Poetry (управление зависимостями)  
- Simple JWT (аутентификация)  

---

## Установка и запуск локально (без Docker)

1. Клонируем репозиторий:

```bash
git clone https://github.com/Chocoeater/Trading-Net.git
git checkout develop
````

2. Устанавливаем Poetry (если ещё не установлен):

```bash
pip install poetry
```

3. Устанавливаем зависимости проекта через Poetry:

```bash
poetry install
```

4. Активируем виртуальное окружение Poetry:

```bash
poetry shell
```

5. Создаем `.env` файл в корне проекта с содержимым (пример):

```env
DEBUG=True
SECRET_KEY=your_secret_key
DB_NAME=task_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=ваш_секретный_ключ
DEBUG=True
```

6. Применяем миграции:

```bash
python manage.py migrate
```

7. Создаем суперпользователя:

```bash
python manage.py create_admin
```

8. Запускаем сервер:

```bash
python manage.py runserver
```

---

## Запуск через Docker Compose (локально)

1. Убедитесь, что установлены Docker и Docker Compose.

2. Собираем и запускаем сервисы:

```bash
docker-compose -f docker-compose.dev.yml up -d --build
```

> Сервис `back` — Django (с Poetry внутри), `db` — PostgreSQL.

3. Создаем суперпользователя в контейнере:

```bash
docker-compose exec back python manage.py create_admin
```

5. Проект доступен на [http://localhost:8000](http://localhost:8000).

---

## Документация API

Используется `drf-spectacular`.

* OpenAPI схема: `/schema/`
* Redoc: `/redoc/`
* Swagger UI: `/swagger/`

Примеры эндпоинтов:

* `/nodes/` — CRUD узлов сети поставок (Node)
* `/products/` — CRUD продуктов

Поддерживается фильтрация, поиск и сортировка через query-параметры.

---

## Тестирование

```bash
pytest
```
---

## Рекомендации по использованию

* Админка доступна через стандартный Django Admin.
* Permission `IsActiveEmployee` ограничивает действия для сотрудников.
* Удаление поставщиков через API запрещено.

---
