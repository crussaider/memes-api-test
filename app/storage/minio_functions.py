from fastapi import UploadFile
from app.storage.minio_client import minio_client, bucket_name
import uuid


def __generate_file_name(original_filename):
    """
    Создает уникальное имя файла на основе исходного имени файла.

    :param original_filename: Исходное имя файла.
    :return: Уникальное имя файла, созданное с использованием UUIDv4 и исходного расширения файла.
    """
    unique_id = uuid.uuid4()
    extension = original_filename.split('.')[-1]
    new_filename = f"{unique_id}.{extension}"
    return new_filename


def upload_file(file: UploadFile, file_name: str):
    """
    Загружает файл в MinIO и возвращает URL-адрес загруженного файла.

    :param file: Файл для загрузки.
    :param file_name: Исходное имя загруженного файла.
    :return: URL-адрес загруженного файла.
    """
    uuid_name = __generate_file_name(file_name)
    minio_client.put_object(
        bucket_name,
        uuid_name,
        file.file,
        length=-1,
        part_size=10 * 1024 * 1024,
        content_type=file.content_type
    )
    return f"http://localhost:9000/{bucket_name}/{uuid_name}"


def update_file(file: UploadFile, file_url: str):
    """
    Обновляет существующий файл в MinIO, замениет его новым файлом и возвращает обновленный URL-адрес файла.

    :param file: Новый файл для замены существующего файла.
    :param file_url: URL-адрес существующего файла в MinIO.
    :return: Обновленный URL-адрес файла после замены.
    """
    delete_file(file_url)
    return upload_file(file, file_name=file.filename)


def delete_file(file_url: str):
    """
    Удаляет файл из MinIO по его URL-адресу.

    :param file_url: URL-адрес файла, который нужно удалить.
    """
    file_name = file_url.split("/")[-1]
    minio_client.remove_object(bucket_name, file_name)