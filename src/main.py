"""
Код приложения Помощник студента
Проектный практикум, группа 5
"""

# импортируем необходимые бибилиотеки
import streamlit as st

from transformers import pipeline


@st.cache_resource
def load_model_summary():
    """
    Функция загружает модель "саммари" через pipeline.
    Декоратор @st.cache_resource необходим для того, чтобы модель загружалась
    один раз при первом посещении страницы и далее подтягивалась из кеша.

    Возможно использование альтернативных моделей:
    'csebuetnlp/mT5_multilingual_XLSum'
    'd0rj/ru-mbart-large-summ'
    """

    model = 'IlyaGusev/mbart_ru_sum_gazeta'
    return pipeline('summarization', model=model)


@st.cache_resource
def load_model_qa():
    """
    Функция загружает модель "вопрос-ответ" по контенту
    также кешируем загрузку модели, для экономии ресурсов через декоратор @st.cache_resource
    """

    return pipeline("question-answering", model="timpal0l/mdeberta-v3-base-squad2")


def get_answer(context, question, st=None):
    """ Выводит найденный ответ в заданном тексте по заданному вопросу.
        Возвращает словарь с найденным ответом и оценкой. Если переменная 
        st == None, то не выводит результат работы в виджет. Такой режим
        используется для программного получения результатов, в частности
        при тестировании приложения.        

    Args:        
        context (str): Текст, в котором ищем ответы.
        question (str): Вопрос, ответ на который хотим получить.
        st (module): Модуль  Streamlit, через который строим интерфейс. Для тестирования None.

    Returns:
        dict: answer (str): Найденный ответ.
              score (float): Оценка верность ответа.
    """

    questioner = load_model_qa()

    result = questioner(question=question, context=context)
    result['answer'] = result['answer'].strip(' ".<>:,=*\n')

    # Если st не задано, то выводить результаты в интерфейс не нужно
    if not st is None:
        # проверяем скор полученного от модели ответа.
        if result['score'] > 0.01:
            # Оценка оказалась приемлемой, выводим ответ пользователю.
            st.write(result['answer'])
            # И отражаем оценку, чтобы пользователь понимал оценочную достоверность ответа.
            st.write('score is: ', result['score'])
        else:
            # Оценка оказалась недопустимо низкой и мы просто сообщаем пользователю, что ответ не найден.
            st.write('не получается найти в тексте достоверный ответ')

    return result


# Делаем условие, чтобы код не отрабатывался во время импорта в другие модули, в частности для тестирования.
if __name__ == '__main__':
    # выводим приверственный тайтл и кратко обозначаем, что делает помощник
    st.title('Привет! Я помощник студенту 🎈')
    st.text('Я умею сокращать текст или искать ответы в нем')

    context_info = st.text_area(
        'Скопируй текст в это поле ввода:', key='context', height=300, max_chars=2000)

    # предлагаем пользователю выбрать, чем он будет пользоваться
    option = st.selectbox(
        'Будем сокращать текст или искать в нем ответы?',
        ('Сокращать', 'Искать ответы'), key='option')

    # проверяем пользовтаельский выбор
    if option == 'Сокращать':
        # пользователь выбрал Сокращать, значит выдаем ему кнопку
        btn1 = st.button("Поехали!", key="summ", type="primary")
        if btn1:
            # пользователь нажал кнопку, но нам нужно проверить, не "пустой" ли контекст, по которому мы собираем сделать саммари

            if len(context_info) > 99:
                # вызываем функции загрузки модели саммари
                summarizer = load_model_summary()

                # запускам модель саммари по введенному пользователем тексту
                result = summarizer(context_info, truncation=True)
                st.write(result[0]['summary_text'])
            else:
                # слишком мало контекста, поэтому выдаем ему предупреждение
                st.write('Текст должен содержать хотя бы 100 символов')
    else:
        # пользователь выбрал "Искать ответы"
        # выводим поле вводя для вопроса для пользователя
        quest = st.text_input('Напиши свой вопрос к тексту: ', max_chars=200)
        # выводим кнопку для запуска модели
        btn2 = st.button("Найди ответ", key="button", type="primary")
        if btn2:
            # пользователь нажал кнопку, запускаем модель QA
            get_answer(context_info, quest, st)
