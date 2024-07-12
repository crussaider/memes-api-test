import minio.error
import sqlalchemy.exc
from fastapi import APIRouter, HTTPException, Query, UploadFile, Depends, status
from sqlalchemy.orm import Session
from app.models.schemas import Meme as MemeSchema, MemeList
from app.models.meme import Meme as MemeModel
from app.dependencies import get_db
from app.storage.minio_functions import upload_file, update_file, delete_file

router = APIRouter(
    prefix="/memes",
    tags=["Memes"],
)


@router.get("/", response_model=MemeList, status_code=status.HTTP_200_OK)
def get_memes(limit: int = Query(default=10, ge=1), offset: int = Query(default=0, ge=0),
              db: Session = Depends(get_db)):
    """
    Получить список мемов с нумерацией страниц

    :param limit: Максимальное число возвращаемых мемов.
    :param offset: Количество мемов, пропускаемых с начала списка.
    :param db: Зависимость сеанса базы данных SQLAlchemy.
    :return: JSON, содержащий список мемов и их общее количество.
    """
    memes = db.query(MemeModel).offset(offset).limit(limit).all()
    total = db.query(MemeModel).count()
    return MemeList(memes=memes, total=total)


@router.get("/{id}", response_model=MemeSchema, status_code=status.HTTP_200_OK)
def get_meme(id: int, db: Session = Depends(get_db)):
    """
    Получить один мем по его идентификатору

    :param id: Идентификатор мема, который нужно получить.
    :param db: Зависимость сеанса базы данных SQLAlchemy.
    :return: JSON, содержащий сведения о запрошенном меме.

    :raises: HTTPException: если мем с указанным идентификатором не существует (404 Not Found).
    """
    meme = db.query(MemeModel).filter(MemeModel.id == id).first()
    if not meme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meme not found")
    return meme


@router.post("/", response_model=MemeSchema, status_code=status.HTTP_201_CREATED)
def create_meme(title: str, file: UploadFile, db: Session = Depends(get_db)):
    """
    Создает новый мем с указанным названием и загруженным файлом.

    :param title: Название нового мема.
    :param file: Загруженный файл изображения.
    :param db: Зависимость сеанса базы данных SQLAlchemy.
    :return: JSON, содержащий сведения о созданном меме.

    :raises: HTTPException: Если при добавлении в базу данных возникла ошибка. (500 Internal Server Error).
    """
    file_url = upload_file(file, file.filename)
    db_meme = MemeModel(title=title, image_url=file_url)
    try:
        db.add(db_meme)
        db.commit()
        db.refresh(db_meme)
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error when adding")
    return db_meme


@router.put("/{id}", response_model=MemeSchema, status_code=status.HTTP_200_OK)
def update_meme(id: int, title: str, file: UploadFile, db: Session = Depends(get_db)):
    """
    Обновляет название и загруженный файл мема по его идентификатору.

    :param id: Идентификатор мема, который необходимо обновить.
    :param title: Обновленное название мема.
    :param file: Обновленный файл изображения.
    :param db: Зависимость сеанса базы данных SQLAlchemy.
    :return: JSON, содержащий сведения об обновленном меме.

    :raises: HTTPException: Если мем с указанным ID не существует (404 Not Found),
    или если возникли ошибки при обновлении в базе данных или MINIO (500 Internal Server Error).
    """
    db_meme = db.query(MemeModel).filter(MemeModel.id == id).first()
    if not db_meme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meme not found")
    try:
        db_meme.title = title
        db_meme.image_url = update_file(file, db_meme.image_url)
        db.commit()
        db.refresh(db_meme)
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error when updating in database")
    except minio.error.S3Error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error when updating in MINIO")
    return db_meme


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meme(id: int, db: Session = Depends(get_db)):
    """
    Удаляет мем по его идентификатору.

    :param id: Идентификатор мема, который нужно удалить.
    :param db: Зависимость сеанса базы данных SQLAlchemy.
    :return: None

    :raises: HTTPException: если мем с указанным идентификатором не существует (404 Not Found),
    или если возникли ошибки при удалении из базы данных или MINIO (500 Internal Server Error).
    """
    db_meme = db.query(MemeModel).filter(MemeModel.id == id).first()
    if not db_meme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meme not found")
    try:
        db.delete(db_meme)
        db.commit()
        delete_file(db_meme.image_url)
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error when deleting from database")
    except minio.error.S3Error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error when deleting from MINIO")
    return None
