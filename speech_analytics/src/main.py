# src/main.py
import os
from src.audio_processing.audio_splitter import split_audio_to_channels
from src.transcriptions.transcriber import transcribe_audio
from src.services.firestore_service import save_transcription_to_firestore
from src.utils.logger import setup_logging

# Настройка логирования
setup_logging()


def main(audio_url, organization_id, output_bucket_name):
    """
    Главная функция для обработки аудио, транскрибации и сохранения результата.

    :param audio_url: URL аудиофайла
    :param organization_id: ID организации
    :param output_bucket_name: Название bucket в GCS для хранения файлов
    """
    # Разделение аудиофайла на левый и правый каналы
    left_channel_url, right_channel_url = split_audio_to_channels(audio_url, output_bucket_name)

    # Транскрибирование каждого канала
    left_transcript = transcribe_audio(left_channel_url, "manager")
    right_transcript = transcribe_audio(right_channel_url, "client")

    # Сохранение результатов в Firestore
    result = save_transcription_to_firestore(
        organization_id=organization_id,
        audio_url=audio_url,
        left_channel_url=left_channel_url,
        right_channel_url=right_channel_url,
        manager_transcript=left_transcript,
        client_transcript=right_transcript
    )

    print(f"Транскрипция успешно сохранена в Firestore: {result}")


if __name__ == "__main__":
    # Входные параметры (можно получить из файла конфигурации или передать через командную строку)
    audio_url = "https://example.com/path/to/audio.wav"
    organization_id = "12345"
    output_bucket_name = "my-audio-bucket"

    main(audio_url, organization_id, output_bucket_name)
