import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(

    page_title = ' !پنل انالیز  ' 

)

st.title('صفحه اصلی')
st.sidebar.success('!صفحه مد نظر خود را باز کنید')


st.warning(' دوستان اینجا درست شده تابتونیم سابقه های معاملاتی رو برسی و شبیه سازی کنیم ')


image = Image.open('mamosh.jpg')

st.image(image, caption='زبور عسل')



