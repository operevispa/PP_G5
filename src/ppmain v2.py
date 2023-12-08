import streamlit as st
import pandas as pd
from transformers import pipeline

@st.cache_resource
def load_model1():
  return pipeline("question-answering", model="timpal0l/mdeberta-v3-base-squad2")

def textcleaner(stcl):
  return stcl.replace("\n","").strip()

pipl = load_model1()

st.title('Привет! Я помощник студенту 🎈')
st.text('Я умею делать саммари статей и отвечать на твои уточняющие вопросы к этой статье')
st.text('Это позволит тебе за секунды понять суть контента и получить ответы на вопросы')

context_info = st.text_area('Скопируй текст в это поле ввода:')
st.write(context_info)

quest = st.text_input('Напиши свой вопрос к тексту: ')
btn2 = st.button("Найди ответ", type="primary")
if btn2:
    if quest:
        result = pipl(question = quest, context = context_info)
        st.write(textcleaner(result['answer']))
        st.write("score is: ", result['score'])