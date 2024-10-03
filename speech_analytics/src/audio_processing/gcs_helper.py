# src/audio_processing/gcs_helper.py
from google.cloud import storage

storage_client = storage.Client()


def upload_to_gcs(file_path, bucket_name):
    """
    Загружает файл в указанный bucket GCS и возвращает публичный URL.

    :param file_path: Путь к файлу на локальной машине
    :param bucket_name: Название bucket в GCS
    :return: Публичный URL файла
    """
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(os.path.basename(file_path))
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url
