"""
Файл тестирования основного приложения. Тестирование интерфейса производится
с использованием AppTest, предоставленного библиотекой Streamlit. Однако некоторые
интерфейсные виджеты перехватить сложно, поэтому для тестирования также используется
прямое обращение к функциям модуля.
"""

from streamlit.testing.v1 import AppTest
from ..src import main


def test_answer():
    """
    Функция проверяет работу функционала по поиску ответов в тексте. Для добавления
    тестов используется список test_list.

    Каждый элемент списка должен содержать словарь со следующими полями:

    context - текст в котором ищем ответ.
    question - вопрос, на который ищем ответ.
    answer - ответ, который должны получить, задавая вопрос.
    score - число, минимальная уверенность, которая допустима при ответе на вопрос.
    """

    test_list = [{"context": "My name is Tim and I live in Sweden.",
                  "question": "Where do I live?", "answer": "Sweden", "score": 0.8},
                 {"context": "My name is Tim and I live in Sweden.",
                  "question": "What is my name?", "answer": "Tim", "score": 0.8}
                 ]

    for valid_rule in test_list:

        # Заполняем исходные данные в поля приложения
        result = main.get_answer(valid_rule['context'], valid_rule['question'])

        assert result['answer'] == valid_rule['answer'], \
            f"""
        Проверка функционала поиска ответов на вопрос не пройдена.
        Ожидаемый ответ: '{valid_rule['answer']}'.
        Полученный ответ: '{result['answer']}'.
        """

        assert result['score'] >= valid_rule['score'], \
            f"""
        Проверка функционала поиска ответов на вопрос не пройдена.
        Ожидаемая оценка: {valid_rule['score']}.
        Полученный ответ: {result['score'] }.
        """


def test_app_run():
    """
    Функция тестирует запуск приложения в целом, а не отдельные возможнос и приложения.
    """

    # Переменная для тестирования интерфейса
    at = AppTest.from_file('src/main.py')
    at.run()

    assert not at.exception


def test_summ():
    """
    Функция тестирует функционал по сокращению текста. Т.к. результат работы модели
    является творческим, то данный тест лишь убеждается, что модель отрабатывает без
    ошибок и выдает на выходе некоторый текст. Текст для тестирования можно менять,
    он находится в файле text_for_test.txt.
    """

    # Считываем текст для тестирования
    with open('test/text_for_test.txt') as f:
        context = f.read()

    # Получаем краткое содержание по тексту.
    result = main.get_sum(context)

    assert isinstance(result, str)
    assert len(result) > 0
