# импортируем необходимые бибилиотеки
import streamlit as st

import searcher

# Создаем заголовок.
st.title('Экспериментальный функционал')

# Выводим краткую инструкцию .
st.text('''
        Помощник студента попробует найти текст и время из видео на YouTube. Стоит учесть,
        что пока поиск работает только с русской речью.

        Для использования необходимо совершить следующие шаги:
        ''')

# Создаем интерфейс для использования
URL_YouTube = st.text_area(
    '1. Введи ссылку с видеороликом. Например, https://www.youtube.com/watch?v=MWGS7xlvJKA', key='URL', max_chars=200)
search_text = st.text_input(
    '2. Введи текст, который будем искать.', key='search_text', max_chars=200)
btn_search = st.button('Найти текст', key='btn_search')

if btn_search:
    # При нажатии кнопки запускаем распознавание текста
    result = searcher.get_timestamp_from_video(URL_YouTube, search_text)
    if len(result) == 0:
        st.write('К сожалению, совпадений не найдено')
    else:
        st.write('''
                 Удалось найти некоторые совпадения. Слева отображается интервал на котором произносится предложение.
                 В предложении подсвечивается текст, который требовалось искать. Для удобства можно сразу перейти к
                 нужному моменту по видео, кликнув на ссылку.
                 ''')
        for el in result:
            # Выводим результаты. Будет выводится тайминг определенного предложения с подсветкой найденной строки,
            # а также кликабельная ссылка, чтобы сразу перейти к нужному интервалу.
            int_time = int(el["time"][0])
            st.write(f'{el["time"]}: {el["sentence"]}')
            st.write(f'{URL_YouTube}#t={int_time // 60}m{int_time % 60}s')
