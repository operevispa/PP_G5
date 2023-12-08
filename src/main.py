# Код приложения Помощник студента
# Проектный практикум, группа 5

# импортируем необходимые бибилиотеки
import streamlit as st
import pandas as pd
from transformers import pipeline

# загружаем модель "саммари" через pipeline
# декоратор @st.cache_resource необходим для того, чтобы модель загружалась один раз при первом посещении страницы
# и далее подтягивалась из кеша
@st.cache_resource
def load_model_summary():  
  # альтернативные модели саммари для тестирования
  # model = "d0rj/ru-mbart-large-summ"
  # model = 'csebuetnlp/mT5_multilingual_XLSum'
  model = "IlyaGusev/mbart_ru_sum_gazeta"
  return pipeline("summarization", model=model)

# загружаем модель "вопрос-ответ" по контенту через pipeline
# также кешируем загрузку модели, для экономии ресурсов
@st.cache_resource
def load_model_qa():
  return pipeline("question-answering", model="timpal0l/mdeberta-v3-base-squad2")

# функция очистки текста от знака переноса и лишних пробелов в начале и конце строки
def textcleaner(stcl):
  return stcl.replace("\n","").strip()

# вызываем функции загрузки моделей
summarizer = load_model_summary()
questioner = load_model_qa()

# выводим приверственный тайтл и кратко обозначаем, что делает помощник
st.title('Привет! Я помощник студенту 🎈')
st.text('Я умею делать саммари текста и отвечать на твои уточняющие вопросы к этому тексту')
# st.text('Это позволит тебе за секунды понять суть контента и получить ответы на вопросы')

context_info = st.text_area('Скопируй текст в это поле ввода:', height=300)

# предлагаем пользователю выбрать, чем он будет пользоваться
option = st.selectbox(
     'Будем делать саммари или задавать вопросы?',
     ('Саммари', 'Вопросы'))

# проверяем пользовтаельский выбор
if option == 'Саммари':
  # пользователь выбрал Саммари, значит выдаем ему кнопку 
  btn1 = st.button("Поехали!", type="primary")
  if btn1:  
    # пользователь нажал кнопку, но нам нужно проверить, не "пустой" ли контекст, по которому мы собираем сделать саммари
    if len(context_info) > 99:
      # запускам модель саммари по введенному пользователем тексту
      result = summarizer(context_info, truncation=True)
      st.write(result[0]['summary_text'])
    else:
      # слишком мало контекста, поэтому выдаем ему предупреждение
      st.write('Текст должен содержать хотя бы 100 символов')
else:
  # пользователь выбрал "Вопросы"
  # выводим поле вводя для вопроса для пользователя
  quest = st.text_input('Напиши свой вопрос к тексту: ')
  # выводим кнопку для запуска модели 
  btn2 = st.button("Найди ответ", type="primary")
  if btn2:
    # пользователь нажал кнопку, запускаем модель QA    
    result = questioner(question = quest, context = context_info)
    # проверяем скор полученного от модели ответа. 
    if result['score'] > 0.01:
      # скор оказался приемлемы, выводим ответ пользователю      
      st.write(textcleaner(result['answer']))
      # и отражаем скор, чтобы пользователь понимал оценочную достоверность ответа
      st.write('score is: ', result['score'])
    else:
      # скор оказался недопустимо низким и мы просто сообщаем пользовтаелю, что ответ не найден
      st.write('не получается найти в тексте достоверный ответ')