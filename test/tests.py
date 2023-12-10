"""
Файл тестирования основного приложения
"""
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("./src/main.py")


def test_answer():
    """
    Функция проверяет работу функционала по поиску ответов в тексте. Для добавления тестов используется список test_list.
    Каждый элемент списка должен содержать словарь со следующими полями:

    context - текст в котором ищем ответ.
    question - вопрос, на который ищем ответ.
    answer - ответ, который должны получить, задавая вопрос.
    score - число, минимальная уверенность, которая допустима при ответе на вопрос.
    """

    test_list = [{"context": "My name is Tim and I live in Sweden.", "question": "Where do I live?", "answer": "Sweden", "score": 0.8},
                 {"context": "My name is Tim and I live in Sweden.",
                     "question": "What is my name?", "answer": "Tim", "score": 0.8}
                 ]

    # Выбираем опцию поиска ответов
    at.selectbox[0].select("Искать ответы")

    for valid_rule in test_list:

        # Заполняем исходные данные в поля приложения
        at.text_area[0].input(valid_rule["context"]).run()
        at.text_input[0].input(valid_rule["question"]).run()
        at.button[0].click().run()

        # assert == valid_rule["answer"]
        # assert >= valid_rule["score"]
