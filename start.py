
import streamlit as st
import pandas as pd
from PIL import Image

def main():
    st.title('صفحه اصلی')

    st.warning('دوستان اینجا درست شده تابتونیم سابقه های معاملاتی رو برسی و شبیه سازی کنیم ')


    image = Image.open('mamosh.jpg')
    st.title('زنبور عسل')
    st.image(image, caption='زبور عسل')


    


if __name__=='__main__':

    st.set_page_config(

        page_title= 'Anal Hist',
        page_icon= 'hot'
        #layout= 'wide'
        )

    main()




