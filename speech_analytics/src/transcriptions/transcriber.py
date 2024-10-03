# src/transcriptions/transcriber.py
from google.cloud import speech

def transcribe_audio(audio_url, speaker_role):
    """
    Транскрибация аудиофайла с использованием Google Speech-to-Text API.

    :param audio_url: URL аудиофайла
    :param speaker_role: Роль спикера (например, "manager" или "client")
    :return: Текстовая транскрипция
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=audio_url)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)

    transcript = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcript
