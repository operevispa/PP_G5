import streamlit as st
import pandas as pd
from transformers import pipeline
import context

@st.cache_resource
def load_model():
  return pipeline("question-answering", model="timpal0l/mdeberta-v3-base-squad2")

def textcleaner(stcl):
  return stcl.replace("\n","").strip()

pipl = load_model()

st.title('Привет! Это команда Проектного практикума, группа 5 🎈')
st.header('Нас в команде 6 человек. Мы пытаемся запилить Помощника для студентов')
st.text('Это тестовый функционал. Задай вопрос, а я попробую ответить:')
st.text('Пример вопроса: какой предмет вы изучаете, кто в команде и тд')

quest = st.text_input('Напиши свой вопрос: ')
if quest:
  result = pipl(question = quest, context = context.context1)
  st.write(textcleaner(result['answer']))
  st.write("score is: ", result['score'])
