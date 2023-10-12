import streamlit as st
import pandas as pd
from PIL import Image


st.title('صفحه اصلی')



st.write(f"Welcome !") 



st.warning('دوستان اینجا درست شده تابتونیم سابقه های معاملاتی رو برسی و شبیه سازی کنیم ')

image = Image.open('mamosh.jpg')

st.image(image, caption='زبور عسل')
st.title('زنبور عسل')
