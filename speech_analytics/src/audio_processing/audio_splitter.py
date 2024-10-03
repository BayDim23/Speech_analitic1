# src/audio_processing/audio_splitter.py
import ffmpeg
import tempfile
import os
from src.audio_processing.gcs_helper import upload_to_gcs


def split_audio_to_channels(audio_url, output_bucket_name):
    """
    Функция для разделения стерео аудио на два моноканала (левый и правый).

    :param audio_url: URL аудиофайла
    :param output_bucket_name: Название bucket для хранения файлов
    :return: Публичные URL разделенных каналов (левого и правого)
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        audio_file_path = temp_audio_file.name
        # Загрузка аудиофайла
        os.system(f"wget {audio_url} -O {audio_file_path}")

        # Разделение на левый и правый каналы
        left_channel_path = f"{audio_file_path}_left.wav"
        right_channel_path = f"{audio_file_path}_right.wav"

        # Использование ffmpeg для разделения каналов
        ffmpeg.input(audio_file_path).output(left_channel_path, ac=1, map_channel="0.0.0").run()
        ffmpeg.input(audio_file_path).output(right_channel_path, ac=1, map_channel="0.0.1").run()

        # Загрузка разделенных аудиофайлов в Google Cloud Storage
        left_channel_url = upload_to_gcs(left_channel_path, output_bucket_name)
        right_channel_url = upload_to_gcs(right_channel_path, output_bucket_name)

        # Удаление временных файлов
        os.remove(audio_file_path)
        os.remove(left_channel_path)
        os.remove(right_channel_path)

        return left_channel_url, right_channel_url
