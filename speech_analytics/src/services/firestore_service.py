# src/services/firestore_service.py
from google.cloud import firestore

db = firestore.Client()

def save_transcription_to_firestore(organization_id, audio_url, left_channel_url, right_channel_url, manager_transcript, client_transcript):
    """
    Сохранение транскрипции в Firestore.

    :param organization_id: ID организации
    :param audio_url: URL оригинального аудиофайла
    :param left_channel_url: URL левого канала
    :param right_channel_url: URL правого канала
    :param manager_transcript: Транскрипция менеджера
    :param client_transcript: Транскрипция клиента
    :return: ID сохраненного документа
    """
    doc_ref = db.collection("transcriptions").add({
        "organization_id": organization_id,
        "audio_url": audio_url,
        "left_channel_url": left_channel_url,
        "right_channel_url": right_channel_url,
        "manager_transcript": manager_transcript,
        "client_transcript": client_transcript
    })
    return doc_ref.id
