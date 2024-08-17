# Habit Tracker API

Этот проект представляет собой бэкенд для трекера полезных привычек, реализованный с использованием Django и Django Rest Framework (DRF).

## Особенности проекта

- Пользователь может создавать и управлять своими привычками.
- Пагинация для списка привычек.
- Напоминания о выполнении привычек с помощью интеграции с Telegram.
- Поддержка отложенных задач через Celery.
- Аутентификация пользователей.
- Публичные и приватные привычки.

### Требования

- Python 
- Django 
- Poetry (для установки зависимостей)
- DRF
- PostgreSQL
- Redis
- Celery
- Docker

## Шаги установки

1. Клонируйте репозиторий:

    ```bash
   git clone git@github.com:meR1D1AN/kur_7_drf
   cd kur_7_drf
   ```

2. Установите зависимости с помощью Poetry:

    ```bash
    poetry install
    ```

3. Настройте файл окружения:

    Скопируйте `.env.sample` в `.env` и настройте переменные окружения в файле `.env`.

    ```bash
    cp .env.sample .env
    ```
   

4. Создание и примените миграции:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
   
5. Для заполнения тестовой базы данных используйте команды:

- Команда для создания обычного пользователя
    ```bash
   python manage.py cu
    ```
- Команда для создания администратора
  ```bash
   python manage.py cu
  ```
- Добавление данных в базу данных  
   ```bash
    python manage.py loaddata fixtures/habits.json
   ```
6. Установите и запустите Redis
    ```bash
    redis-server
    ```
7. Для запуска проект необходимо выполните команду:
    ```bash
    python manage.py runserver
    ```
8. Для запуска Celery Worker и Celery Beat необходимо выполнить следующие команды:
    - для запуска Celery Worker на Linux:
   ```bash
    celery -A config worker -l INFO
   ```
   - для запуска Celery Worker на Windows:
   ```bash
   celery -A config worker -l INFO -P eventlet
   ```
   - для запуска Celery Beat необходимо открыть дополнительный терминал, и ввести следующую команду на Windows:
   ```bash
   celery -A config beat -l info -S django
   ```
   - для запуска Celery Worker и Celery Beat на Linux, используйте следующую команду:
   ```bash
   celery -A config worker --beat --scheduler django
   ```

## Использование

- Регистрация и аутентификация
- Зарегистрируйте нового пользователя через /api/users/registration/.
- Авторизуйтесь через /api/users/login/.
- Работа с привычками
- Создать привычку: POST /api/habits/
- Получить список привычек: GET /api/habits/
- Получить детальную информацию о привычке: GET /api/habits/{id}/
- Обновить привычку: PATCH /api/habits/{id}/
- Удалить привычку: DELETE /api/habits/{id}/

### Интеграция с Telegram
- Настройте Telegram-бота для отправки уведомлений о привычках.
- Задачи Celery
- Используйте Celery для выполнения отложенных задач, например, отправки уведомлений.

### Тестирование

1. Запустите тесты (внесены исключения для тестирования, такие как миграции, и файлы в папке config)

```bash
coverage run --source='.' --omit='*/migrations/*,config/agsi.py,config/wsgi.py' manage.py test
coverage report
```
2. Запустите проверку flake 8. (добавлен файл .flake8 в нём внесены исключения для проверки)
```bash
flake8 .
```

## Документация API
