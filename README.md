# Meme API

## Описание

Это Python 3.11 веб-приложение на FastAPI, которое предоставляет API для работы с коллекцией мемов. Приложение состоит из двух сервисов: сервис с публичным API с бизнес-логикой и сервис для работы с медиа-файлами, используя S3-совместимое хранилище MinIO.

## Функциональность

- **GET /memes**: Получить список всех мемов (с пагинацией).
- **GET /memes/{id}**: Получить конкретный мем по его ID.
- **POST /memes**: Добавить новый мем (с картинкой и текстом).
- **PUT /memes/{id}**: Обновить существующий мем.
- **DELETE /memes/{id}**: Удалить мем.

С более подробным описанием endpoint-ов можно ознакомиться в документации `http://localhost:8000/docs` или `http://localhost:8000/redoc`

## Запуск для разработки

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/crussaider/memes-api-test.git
    cd memes-api-test
    ```

2. Запустите Docker Compose:
    ```bash
    docker-compose up --build
    ```

3. Откройте в браузере:
    ```plaintext
    http://localhost:8000/docs
    ```

## Тестирование

После запуска PostgreSQL, MinIO и FastAPI можно запустить тесты с помощью `pytest`:
```bash
python -m venv venv
venv\Scripts\activate.bat # Windows
pip install -r requirements.txt
pytest
```
```bash
python -m venv venv
source venv/bin/activate # Linux
pip install -r requirements.txt
pytest
```