from app.db.database import SessionLocal


def get_db():
    """
    Зависимость для получения сеанса базы данных SQLAlchemy.

    :return: Экземпляр сеанса SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
