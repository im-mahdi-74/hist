import streamlit as st
import pandas as pd
from PIL import Image


from streamlit import session_state as session

# تابع مدیریت session
def session_manager():
  if "username" not in session:
    session.username = st.text_input("Enter username")  

st.title('صفحه اصلی')

session_manager()

st.write(f"Welcome {session.username}!") 



st.warning('دوستان اینجا درست شده تابتونیم سابقه های معاملاتی رو برسی و شبیه سازی کنیم ')

image = Image.open('mamosh.jpg')

st.image(image, caption='زبور عسل')
st.title('زنبور عسل')
