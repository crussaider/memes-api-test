from fastapi import FastAPI
from app.routers import meme_router

app = FastAPI(
    title="Meme API",
    description="Тестовое задание. Веб-приложение, которое предоставляет API для работы с коллекцией мемов.",
    contact={
        "name": "Dmitry Ryapalov",
        "email": "dimaryapalov@gmail.com",
    }
)

tags_metadata = [
    {
        "name": "Root",
        "description": "Начальная страница.",
    },
    {
        "name": "Memes",
        "description": "Операции с мемами.",
    },
]

# Подключение роутера
app.include_router(meme_router.router)


@app.get("/", tags=['Root'])
def welcome_message():
    return {"message": "Meme API"}
