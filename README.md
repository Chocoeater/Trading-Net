# TradingNet
Веб-приложение для управления сетью поставщиков и продуктов. Реализовано на Django с использованием DRF и PostgreSQL. Поддерживает API с фильтрацией, поиском и ограничениями доступа для сотрудников.
---
Автор: Коурдаков Илья
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
docker-compose -f docker-compose.yml up -d --build
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
## Основной функционал

Приложение состоит из двух ключевых доменов:

### **1. Suppliers (Поставщики)**  
Главная модель `Node`.  
Каждый поставщик содержит:

- `name` название  
- `email` контакт  
- `country`, `city`, `address`  локация  
- `supplier` родительский поставщик (для построения сети)  
- `debt` долг родителю  
- `created_at`, `updated_at` контроль изменений  

Система позволяет строить многоуровневые цепочки поставок:

```
Sony Japan
└── Sony Europe
├── Sony Poland
└── Sony Germany
```

При этом реализована защита от циклов (невозможно сделать ребёнка родителем).

---

### **2. Products (Продукты)**  
Каждый продукт связан с конкретным поставщиком.

Модель включает:

- `name` название  
- `model` артикул/код  
- `release_date` дата выхода  
- `owner` поставщик–владелец  

Удаление поставщика автоматически удаляет связанные продукты.

---

## 🧬 Примеры работы API

### Создание поставщика

```http
POST /api/nodes/
{
  "name": "Sony Japan",
  "email": "jp@sony.com",
  "country": "Japan",
  "city": "Tokyo",
  "address": "1-7-1 Konan"
}
```
### Добавление дочернего узла

```http
POST /api/nodes/
{
  "name": "Sony Europe",
  "email": "eu@sony.com",
  "country": "Netherlands",
  "city": "Amsterdam",
  "address": "Evert van de Beekstraat 1",
  "supplier": 1
}
```
### Добавление продукта
```http
POST /api/products/
{
  "name": "PlayStation 5",
  "model": "CFI-1216A",
  "release_date": "2020-11-12",
  "owner": 2
}
```

---

## Бизнес-логика и ограничения
Приложение содержит важные валидаторы:

- Предотвращение циклов
Нельзя указать родителем собственный дочерний узел.

- Долг ≥ 0
Отрицательные значения отклоняются.

- Каскадное удаление продуктов
При удалении поставщика удаляются все связанные продукты.

Структура проекта
```bash
TradingNet/
├── config/                # Django-настройки
├── suppliers/             # Поставщики и продукты
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── users/                 # Пользователи и авторизация
│   ├── models.py
│   ├── serializers.py
│   └── management/
└── ...
```

## Пользователи и авторизация
Приложение включает модуль users:

- регистрация

- авторизация (JWT, SimpleJWT)

- обновление профиля

- удаление (soft-delete)

- команда python manage.py create_admin


