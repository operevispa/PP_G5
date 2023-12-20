"""
Модуль предоставляет интерфейс для поиска текста внутри видео-файлов.
Реализован поиск текста через переданный URL на видео-ресурсе YouTube.

Данная функциональность является экспериментальной.
"""

import streamlit as st
import torchaudio
from transformers import pipeline
from transformers import WhisperTokenizer
from pytube import YouTube


@st.cache_resource
def load_model_recognition():
    """
    Подготавливает и кэширует модель средствами Streamlit

    Returns:        
        Pipeline: Подготовленная модель с преднастройками
    """

    model_name = 'openai/whisper-base'
    # Т.к. мы используем проекты только на виртуальных машинах без GPU,
    # то использование модели только с помощью CPU
    device = "cpu"

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model_name,
        chunk_length_s=30,
        device=device, generate_kwargs={
            "task": "transcribe", "language": "<|ru|>"}
    )

    return pipe


def get_audiofile_from_youtube(URL):
    """
    Получает аудиоданные из видеоролика, распложенному на ресурсе YouTube
    по адресу URL и сохраняет их в файл.

    Args:
        URL (str): Адрес видеоролика

    Returns:
        str: Путь до файла, куда сохранено аудио.
    """

    # Используя библиотеку pytube, подключаемся к стриму и выбираем только аудио
    yt = YouTube(URL)
    audio = yt.streams.filter(only_audio=True).first()

    # Записываем аудиопоток в файл
    out_file = audio.download(filename='youtube_audio', output_path=".cache")

    return out_file


def prepare_audio(file):
    """
    Преобразует аудиоданные из файла в словарь, пригодный для использования в моделях.
    В качестве элементов словаря присутствуют аудиоданные в виде массив и частота.

    Args:
        file (str): Путь до файла, содержащего аудио.

    Returns:
        dict: array - аудиоданные, sampling_rate - частота
    """

    # Преобразуем аудиофайл в данные, пригодные для моделей
    tensor, sampling_rate = torchaudio.load(file)
    sample = {'array': tensor.numpy()[0], 'sampling_rate': sampling_rate}

    return sample


def get_timestamp_from_video(URL, search_text):
    """
    Возвращает список найденных предложений вместе с метками времени.

    Args:
        URL (str): URL на видеохостинг YouTube
        search_text (str): Текст, который ищем

    Returns:
        dict: 
            time(tuple) - Время начала и конца отрезка.
            sentence(str) - Предложение, в котором найден текст            
    """

    # Для регистронезависимого поиска будем использовать нижний регистр
    search_text = search_text.strip().lower()
    len_search = len(search_text)

    audiofile = get_audiofile_from_youtube(URL)
    sample = prepare_audio(audiofile)

    pipe = load_model_recognition()
    text_with_timestamp = pipe(
        sample.copy(), batch_size=8, return_timestamps=True)["chunks"]

    result = []
    for snt_with_time in text_with_timestamp:

        time = snt_with_time['timestamp']
        snt = snt_with_time['text']

        f_index = snt.lower().find(search_text)
        if f_index >= 0:
            # Подсвечиваем найденный текст в исходном предложении через синтаксис markdown
            format_snt = snt[:f_index] + '**' + snt[f_index:f_index +
                                                    len_search] + '**' + snt[f_index + len_search:]
            result.append({'time': time, 'sentence': format_snt})

    return result
