import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import io 
import numpy as np
import plotly.graph_objects as go
from datetime import timedelta
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import threading as td
import os
#def num trade in 
dff = None


    



def analhist(file_list):
    try:
        for i in file_list:
            df = pd.read_csv(i, delimiter=';')
            df = df[::-1]
            df['Time']    = pd.to_datetime(df['Time'])
            df['Time_1']  = pd.to_datetime(df['Time.1'])
            df            = df.rename(columns={'Price.1': 'Price_1'})
            df['Profit']  = df['Profit'].astype(str).str.replace(' ', '')
            df['Profit']  = pd.to_numeric(df['Profit'].str.replace(' ', ''), errors='coerce')
            df['Price_1'] = df['Price_1'].astype(str).str.replace(' ', '')
            df['Price_1'] = pd.to_numeric(df['Price_1'].str.replace(' ', ''), errors='coerce')
            df['Price']   = df['Price'].astype(str).str.replace(' ', '')
            df['Price']   = pd.to_numeric(df['Price'].str.replace(' ', ''), errors='coerce')
            df['name'] = i
            #num = 0
            num2 = 0
            balance = 0
            a = 0
            for index, row in df.iterrows():
                a = a+1
                if row['Type'] != 'Balance' and num2 == 0:
                    num = num + 1
                    print(f'bog for {i} csv ; no balance start and remove')
                    break

                if row['Type'] == 'Balance':

                    balance = row['Profit']
                    num2 = num2 + 1
                    df = df.drop(df.index[0])
                    continue

                if num2 != 0:
                    if row['Type'] not in ['Buy', 'Sell']:
                        df = df.drop(index)
                        continue
                    balance = balance + df.at[index , 'Profit']                    
                    df.at[index, 'balance']                = balance
                    df.at[index, 'ABSPP']                  = abs(row['Profit'] * 100) / balance
                    df.at[index, 'PP']                     = (row['Profit'] * 100) / balance
                    
                    if (row['Time_1'] - row['Time']).total_seconds() > 0 :
                        df.at[index, 'delta'] = (row['Time_1'] - row['Time']).total_seconds()
                    else:
                        df.at[index, 'delta'] = 1 


                    df.at[index, 'ABSpipeg']               = abs(row['Price_1'] - row['Price']) * 1000
                    df.at[index, 'V/B']                    = (row['Volume'] * 100000) / balance

                    if row['Price_1'] - row['Price'] == 0:
                        df.at[index, 'ABSpipeg'] = 0

                    if row['Price_1'] - row['Price'] > 0:
                        if row['Type'] == 'Buy':
                            df.at[index, '+pipeg']         = row['Price_1'] - row['Price'] * 1000            
                            df.at[index, '+pipeg/delta']   = df.at[index, '+pipeg'] / df.at[index, 'delta']
                            df.at[index, '+pipeg/Balance'] = df.at[index, '+pipeg'] / balance
                            df.at[index, '+pipeg/VB']      = df.at[index, '+pipeg'] / df.at[index, 'V/B']
                            

                        if row['Type'] == 'Sell':
                            df.at[index, '-pipeg']         = row['Price_1'] - row['Price'] * 1000
                            df.at[index, '-pipeg/delta']   = df.at[index, '-pipeg'] / df.at[index, 'delta']
                            df.at[index, '-pipeg/Balance'] = df.at[index, '-pipeg'] / balance
                            df.at[index, '-pipeg/VB']      = df.at[index, '-pipeg'] / df.at[index, 'V/B']

                    if row['Profit'] > 0:
                        df.at[index, '+P']                 = df.at[index, 'Profit']
                        df.at[index, '+PP']                = abs(df.at[index, '+P'] * 100) / balance
                        df.at[index, '+PPVB']              = df.at[index, '+PP'] / df.at[index, 'V/B']
                        df.at[index, '+PP/delta']          = df.at[index, '+PP'] / df.at[index, 'delta']

                    if row['Profit'] < 0:
                        df.at[index, '-P']                 = df.at[index, 'Profit']
                        df.at[index, '-PP']                = abs(df.at[index, '-P'] * 100) / balance
                        df.at[index, '-PPVB']              = df.at[index, '-PP'] / df.at[index, 'V/B']
                        df.at[index, '-PP/delta']          = df.at[index, '-PP'] / df.at[index, 'delta']

                    if row['Profit'] == 0:
                        df.at[index, 'P'] = df.at[index, 'Profit']

                    df.at[index, 'ABSPP%VB']               = (df.at[index, 'ABSPP'] * 100) / (df.at[index, 'V/B'])
                    df.at[index, 'delta/VB']               =  df.at[index, 'delta'] / (df.at[index, 'V/B'])
                    df.at[index, 'ABSPP/delta']            =  df.at[index, 'ABSPP'] / df.at[index, 'delta']
                    
            df = df[::-1]
            df.to_csv('data.csv', mode='w', index = False)
            
            return df 
            
    except ValueError as er:
        (er)
def timePPm(df):
    st.write('             جدول ترکیب شده سابقه های معاملاتی ')
    
    #df = pd.read_csv('data.csv')
    

    df = df[df['Time'] != 'Time']
    df = df.sort_values(by = 'Time')
    df

    df['Time'] = pd.to_datetime(df['Time']) 

    df_start = df['Time'].min() 
    df_end = df['Time'].max()   

    st.write('#بازه زمانی مورد نظر رو انتخاب کن')
    # کوچکترین تاریخ
    min_date = df['Time'].min()

    # بزرگترین تاریخ
    max_date = df['Time'].max()


    start_date = min_date + timedelta(days=1)
    end_date = max_date - timedelta(days=1)

    date_diff = end_date - start_date 

    if date_diff <= timedelta(days=30):
        # اختلاف کمتر از 30 روز
        # تغییری نده
        # تاریخ شروع را به یک روز بعد از کوچکترین تاریخ تنظیم کنید
        start_date = min_date + timedelta(days=1)
    else:
    # اختلاف بیشتر از 30 روز 
        start_date = end_date - timedelta(days=30)




    # تنظیم مقادیر پیش‌فرض برای کلیدهای تاریخی
    
    start_date = pd.to_datetime(st.date_input(f'Start Date  {df_start}', value=start_date))
    end_date = pd.to_datetime(st.date_input(f'End Date    {df_end}', value=end_date))
    

    #start_date = pd.to_datetime(st.date_input(f'Start Date  {df_start}', value=df_start))
    #end_date = pd.to_datetime(st.date_input(f'End Date    {df_end}', value=df_end))




        
        # چک کردن محدوده
    if start_date < df_start or end_date > df_end:
        st.error("لطفا تاریخی انتخاب کنید بین بازه زمانی   %s       و      %s  " % (df_start, df_end))

    else:
        mask = (df['Time'] > start_date) & (df['Time'] <= end_date)
        filtered_df = df.loc[mask]
        #size = st.slider('Chart Size', min_value=200, max_value=1000, value=400)
        #fig = px.scatter_gl(filtered_df, x='Time', y='PP', height=600)
        global ass
        ass = True
        
        return filtered_df

def inside(df):

    for index, row in df.iterrows():
        df.at[index,'ABSPP']                  = abs(df.at[index,'Profit'] * 100) / df.at[index,'balance']
        df.at[index,'PP']                     =    (df.at[index,'Profit'] * 100) / df.at[index,'balance']
        df.at[index,'V/B']                    =    (df.at[index,'Volume'] * 100000) / df.at[index,'balance']

        df.at[index,'+pipeg/Balance']        = df.at[index,'+pipeg'] / df.at[index,'balance']
        df.at[index,'+pipeg/VB']             = df.at[index,'+pipeg'] / df.at[index,'V/B']
        
        df.at[index,'-pipeg/Balance']        = df.at[index,'-pipeg'] / df.at[index,'balance']
        df.at[index,'-pipeg/VB']             = df.at[index,'-pipeg'] / df.at[index,'V/B']

        df.at[index,'+PP']                   = abs(df.at[index,'+P'] * 100) / df.at[index,'balance']
        df.at[index,'+PPVB']                 = df.at[index,'+PP'] / df.at[index,'V/B']
        df.at[index,'+PP/delta']             = df.at[index,'+PP'] / df.at[index,'delta']

        df.at[index,'-PP']                   = abs(df.at[index,'-P'] * 100) / df.at[index,'balance']
        df.at[index,'-PPVB']                 = df.at[index,'-PP'] / df.at[index,'V/B']
        df.at[index,'-PP/delta']             = df.at[index,'-PP'] / df.at[index,'delta']

        df.at[index,'ABSPP%VB']               = (df.at[index,'ABSPP'] * 100) / (df.at[index,'V/B'])
        df.at[index,'delta/VB']               =  df.at[index,'delta'] / (df.at[index,'V/B'])
        df.at[index,'ABSPP/delta']            =  df.at[index,'ABSPP'] / df.at[index,'delta']


    return df

def mainchart(df): #timePPm()
    win        = (df['Profit'] > 0).sum()
    loss       = (df['Profit'] < 0).sum()
    winrate    = (win * 100) / (win + loss)
    trades     = len(df)
    besttrade  = df['PP'].max()
    worsttrade = df['PP'].min()
    avgtimetrade = df['delta'].mean()
    longtrade  = (df['Type'] == 'Buy').sum()
    shorttrade = (df['Type'] == 'Sell').sum()
    avgProfit  = df['+PP'].mean()
    avgLoss    = df['-PP'].mean()
    avgVB      = df['V/B'].mean()

    # عنوان
    st.title("آمار و اطلاعات معاملات") 

    # ستون‌بندی
    col1, col2 = st.columns(2)

    # ستون اول  
    with col1:
        st.metric("تعداد معاملات", trades)
        st.metric("درصد موفقیت", f"{winrate:.2f}%")
        st.metric("میانگین سود", f"{avgProfit:.2f}")
        st.metric("میانگین زمان", f"{avgtimetrade:.2f}")
    
    # ستون دوم
    with col2:
        st.metric("بهترین معامله", f"{besttrade:.2f}%")
        st.metric("بدترین معامله", f"{worsttrade:.2f}%")  
        st.metric("میانگین ضرر", f"{avgLoss:.2f}%")
        st.metric("میانگین حجم به موجودی", f"{avgVB:.2f}%")

    # جدا کننده
    st.markdown("---")

    # دو ستون 
    left, right = st.columns(2)

    # ستون سمت چپ
    with left:
        st.info(f"تعداد معاملات خرید: {longtrade}")

    # ستون سمت راست   
    with right:
        st.info(f"تعداد معاملات فروش: {shorttrade}")
    
    # نمودار دایره‌ای    
    fig = px.pie(
        values=[win, loss],
        names=['سودده', 'ضررده'],
        color_discrete_map={
            'سودده': 'green',
            'ضررده': 'red'
        }
    )
    st.plotly_chart(fig)

    # نمایش دیتافریم   
    st.dataframe(df.head())

    
        
def p_chart(df):
    st.title('نمودار تایپ معاملات ')

    result = df.groupby(['Symbol', 'Type']).size().unstack(fill_value=0)

    # اضافه کردن نتایج به دیتافریم اصلی به صورت افقی
    df = df.join(result, on='Symbol', rsuffix='_count')
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset=['Symbol'])
    st.bar_chart(df,x='Symbol', y =['Buy', 'Sell'] , width=0, height=700 )
    
def pp_chart(df):

    result = df.groupby(['Symbol', 'Type']).size().unstack(fill_value=0)

    # اضافه کردن نتایج به دیتافریم اصلی به صورت افقی
    df = df.join(result, on='Symbol', rsuffix='_count')
    
    #df = df.drop_duplicates(subset=['Symbol'])
    df['+PPsum'] = df['+PP'].sum()
    df['-PPsum'] = df['-PP'].sum()
    df = df.drop_duplicates()
    st.bar_chart(df,x='Symbol', y =['-PPsum','+PPsum'] , width=0, height=700 )

def pp1_chart(df):

    result = df.groupby(['Symbol', 'delta']).size().unstack(fill_value=0)

    # اضافه کردن نتایج به دیتافریم اصلی به صورت افقی
    df = df.join(result, on='Symbol', rsuffix='_count')
    

    df = df.drop_duplicates()
    df['Hdelta'] = df['delta']/3600
    st.bar_chart(df,x='Symbol', y = 'Hdelta', width=0, height=700 )

def pp2_chart(df):

    result = df.groupby(['Symbol', 'V/B']).size().unstack(fill_value=0)

    # اضافه کردن نتایج به دیتافریم اصلی به صورت افقی
    df = df.join(result, on='Symbol', rsuffix='_count')
    

    df = df.drop_duplicates()
    
    st.bar_chart(df,x='Symbol', y = 'V/B', width=0, height=700 )

def pp3_chart(df):
    df['cospp'] = df['PP'].cumsum()
    df['cosvb'] = df['V/B'].cumsum()
    st.line_chart(df , x = 'Time' , y= 'cospp' ,  width=0, height=700)

def main_chart_one(df):
    # چارت حجم بر زمان         چارت تعداد معاملات باز بر زمان 
    df['Volume'] = df['Volume'].astype(float)
    df['Time']    = pd.to_datetime(df['Time'])
    df['Time_1']  = pd.to_datetime(df['Time.1'])
    start_time = df['Time'].min() 
    end_time = df['Time_1'].max()

    times = pd.date_range(start=start_time, end=end_time, freq='10T')

    chart_df = pd.DataFrame()

    chart_df['Time'] = times
    chart_df['Volume'] = 0
    chart_df['Volume'] = chart_df['Volume'].astype(float)

    chart_df['OpenTrades'] = 0 
    chart_df['OpenTrades'] = chart_df['OpenTrades'].astype(float)
    
    st.text(f'بازه زمانی شما تشکیل شده از {len(times)} سطر لطفا لحظاتی صبر کنید که پردازش تموم بشه ممنون ')
    progress_text = "لطفا صبر کنید "
    my_bar = st.progress(0, text=progress_text)
    
    etr = len(times) / 100
    a = 0
    b = 0
    for  t in tqdm(times, desc="Creating chart"):
        if a == etr :
            
            my_bar.progress(b , text=progress_text)
            b = b+1
            a = 0
        volume = 0
        open_trades = 0
        
        
        a = a+1
        if (df['Time'].apply(lambda x: x <= t)).any() or (df['Time_1'].apply(lambda x: t <= x)).any():
            volume      = df.loc[(df['Time'] <= t) & (t <= df['Time_1']), 'Volume'].sum()
            open_trades = df.loc[(df['Time']<=t) & (t<=df['Time_1'])].shape[0]

        chart_df.loc[chart_df['Time']==t, 'Volume'] = volume
        chart_df['Volume'] = chart_df['Volume'].astype(float)

        chart_df.loc[chart_df['Time']==t, 'OpenTrades'] = open_trades
        chart_df['OpenTrades'] = chart_df['OpenTrades'].astype(float)

    
    st.line_chart(chart_df, x = 'Time' , y = 'Volume' , width=0, height=700 )
    
    st.line_chart(chart_df, x = 'Time' , y = 'OpenTrades' , width=0, height=700 )

def chart_in_b(df , b):

    for index, row in df.iterrows():

        df.at[index , 'newProfit'] = (df.at[index , 'PP'] * b) / 100
        df['cosnewProfit'] = df['newProfit'].cumsum()

    st.line_chart(df , x= 'Time' , y= 'cosnewProfit' ,  width=0, height=700 )

def main_change(df, selected_symbols,selected_symbols_two):

    # حذف نماد 
    
    
    
    df_copy = df.copy()
    
    
    df_copy = df_copy[~df_copy['Symbol'].isin(selected_symbols)]
    
    
    st.write("دیتافریم پس از حذف:")
    df = df_copy


    # تغییر مقادیر مطابق با انتخاب کاربر
    for symbol in selected_symbols_two:
        # تغییر مقادیر ستون Type
        df.loc[df['Symbol'] == symbol, 'Type'] = 'Buy' if df.loc[df['Symbol'] == symbol, 'Type'].any() == 'Sell' else 'Sell'
        # معکوس کردن مقادیر ستون Profit
        df.loc[df['Symbol'] == symbol, 'Profit'] = -df.loc[df['Symbol'] == symbol, 'Profit']
        df.loc[df['Symbol'] == symbol, 'PP'] = -df.loc[df['Symbol'] == symbol, 'PP']
    
    intbalance = 0
    z_row = 0
    for index, row in df.iterrows():
        
        if z_row == 0 :
            df.at[index , 'balance'] = df.at[index , 'balance'] + df.at[index , 'Profit'] 
            intbalance = df.at[index , 'balance']
        else:
            df.at[index , 'balance'] = intbalance + df.at[index , 'Profit']
            intbalance = df.at[index , 'balance']

            
    # نمایش دیتافریم تغییر یافته
    df

    df.to_csv('data_tow.csv', index=False)
    # تغییر حجم نماد یا کل 


    # فیلتر زمان معاملات 








def m_chart(df): #timePPm()

  columns = df.columns.tolist()

  x_column = st.selectbox('Select column for X', columns)
  y_column = st.selectbox('Select column for Y', columns)  

  if st.radio('Select chart type', ['Line', 'Scatter']) == 'Line':
    fig = go.Figure(data=go.Scatter(x=df[x_column], y=df[y_column]))
    fig.update_layout(width=1000, height=500)
    st.plotly_chart(fig)

  else:
    fig = go.Figure(data=go.Scattergl(x=df[x_column], 
                                     y=df[y_column]))
    fig.update_layout(width=1000, height=500)
    st.plotly_chart(fig)








st.title('اینجا میتونی هیستوری سیگنال ها رو اپلود کنی')

uploaded_files = st.file_uploader("هیستوری ها رو انتخاب کن", accept_multiple_files=True, type=['csv'])


if uploaded_files:


    for file in uploaded_files: 
        df = pd.read_csv(io.StringIO(file.read().decode('utf-8')) , delimiter=';') 
        df
        file_name = file.name
        df.to_csv(file_name ,sep = ';', index=False )
        # دسترسی به لیست آدرس فایل ها


    st.title('Process Selected Files')

    selected_files = st.multiselect('Select files', uploaded_files)
    
    filelist = []
 
    
    if st.button('Process Selected Files'):
        file_name = 'data.csv'

        # اگر فایل "data.csv" در همان دایرکتوری اسکریپت وجود دارد، آن را پاک کنید
        if os.path.exists(file_name):
            os.remove(file_name)
        for file in selected_files:
            st.write(f'name file : {file.name}','.....', f'size : {file.size}k')
            filelist.append(file.name)
            # نام فایل برای پاک کردن

        analhist(filelist)




if os.path.exists('data.csv'):
    dff = pd.read_csv('data.csv')
    b =timePPm(dff) 
    d = inside(b)
    d


    if st.button('اطلاعات اماری ' , key = 'anal' ):
        mainchart(d)


    if st.button('بار چارت معاملات ' , key = 'anal1' ): 

        p_chart(d)

    if st.button('سود ضرر درصدی هر نماد ' , key = 'anal2' ):
        pp_chart(d)
    
    if st.button('مجموع مدت زمان معامله هر نماد ' , key = 'anal3' ):
        pp1_chart(d)

    if st.button('نسبت حجم معامله به موجودی برای هر نماد ' , key = 'anal4' ):
        pp2_chart(d)

    if st.button('لاین چارت سود درصدی به زمان ' , key = 'anal5' ):
        pp3_chart(d)

    if st.button('حجم و معاملات باز بر زمان ' , key = 'anal6' ):
        main_chart_one(d)
        
    number = st.number_input("Insert a number", key= 'anal_1')
    st.write('The current number is ', number)    
    if st.button('چارت سود با عدد دلخواه' , key = 'anal7' ):

        chart_in_b(d , number)

    n = d['Symbol'].unique()
    st.text(f'نماد های موجود این ها هستن لطفا اگر میخاهی نمادی رو معکوس کنی حذف نکن  {n}')
    selected_symbols = st.multiselect("انتخاب اسمبل‌ها:", d['Symbol'].unique(),key = 'main_change')       
    nn = d['Symbol'].unique()
    st.text(f'نماد های مورد نظر برای معکوس سازی رو انتخاب کن  {nn}')
    selected_symbols_two = st.multiselect("انتخاب نماد ها:", d['Symbol'].unique() , key = 'main_change_two')
    if st.button(' اعمال حذف و معکوس سازی در دیتافرم' , key = 'anal8' ):
        if os.path.isfile('data_tow.csv' ):
            os.remove('data_tow.csv')
        main_change(d, selected_symbols,selected_symbols_two)




if os.path.exists('data_tow.csv'):
    st.header('انجام فرایندهای تحلیل رو دیتافرم شخصی سازی شده ')
    dfff = pd.read_csv('data_tow.csv')
    bb =timePPm(dfff) 
    dd = inside(bb)
    dd

    if st.button('اطلاعات اماری ' , key = 'ass1' ):
        mainchart(dd)


    if st.button('بار چارت معاملات ' , key = 'ass2' ): 

        p_chart(dd)

    if st.button('سود ضرر درصدی هر نماد ' , key = 'ass3' ):
        pp_chart(dd)
    
    if st.button('مجموع مدت زمان معامله هر نماد ' , key = 'ass4' ):
        pp1_chart(dd)

    if st.button('نسبت حجم معامله به موجودی برای هر نماد ' , key = 'ass5' ):
        pp2_chart(dd)

    if st.button('لاین چارت سود درصدی به زمان ' , key = 'ass6' ):
        pp3_chart(dd)

    if st.button('حجم و معاملات باز بر زمان ' , key = 'ass7' ):
        main_chart_one(dd)
        
    numberr = st.number_input("Insert a number" , key= 'ass_1')
    st.write('The current number is ', numberr)    
    if st.button('چارت سود با عدد دلخواه' , key = 'ass8' ):

        chart_in_b(dd , numberr)

















    



