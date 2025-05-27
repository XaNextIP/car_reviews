# 🚘 Car Reviews API

Проект представляет собой API для управления странами, производителями автомобилей, моделями машин и комментариями пользователей. Построен на **Django + Django REST Framework**, использует **Docker**, **PostgreSQL**, **Token Authentication**.

---

## 🔧 Стек технологий

- Python 3.10
- Django 3.2
- djangorestframework 3.12.4
- psycopg2-binary 2.9.1
- python-dotenv 0.19.0
- openpyxl 3.0.9
- django-filter 21.1

---

## ⚙️ Установка и запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/XaNextIP/car_reviews.git
cd car_reviews
```

### 2. Запустить проект через Docker

```bash
docker-compose up --build
```

> При первом запуске автоматически создаётся суперпользователь:

- **username:** `admin`
- **password:** `admin123!`

---

## 🔐 Аутентификация и токен

### Получить токен:

**POST** `/api/token/`  
**Тело запроса (JSON):**
```json
{
  "username": "admin",
  "password": "admin123!"
}
```

**Ответ:**
```json
{
  "token": "ВАШ_ТОКЕН"
}
```

### Использование токена:

Добавляйте токен в заголовки всех защищённых запросов:

```
Authorization: Token ВАШ_ТОКЕН
```

---

## 📬 Основные эндпоинты API

Базовый путь: `http://localhost:8000/api/`

### 🔹 `/api/countries/`

- `GET` — список стран
- `POST` — создать страну (нужен токен)
- `PUT/PATCH` — обновить страну (нужен токен)
- `DELETE` — удалить страну (нужен токен)

### 🔹 `/api/manufacturers/`

- `GET` — список производителей
- `POST` — создать производителя (нужен токен)
- `PUT/PATCH` — обновить (нужен токен)
- `DELETE` — удалить (нужен токен)

### 🔹 `/api/cars/`

- `GET` — список автомобилей
- `POST` — создать автомобиль (нужен токен)
- `PUT/PATCH` — обновить (нужен токен)
- `DELETE` — удалить (нужен токен)

**Дополнительно:**
- `manufacturer` — указывается как строка (название)
- Возвращаются: `manufacturer_id`, `manufacturer_name`, `comment_count`

### 🔹 `/api/comments/`

- `GET` — список комментариев (публично)
- `POST` — создать комментарий (публично)
- `PUT/PATCH` — редактировать (нужен токен)
- `DELETE` — удалить (нужен токен)

---
