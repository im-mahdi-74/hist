
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io 
from datetime import timedelta
import matplotlib.pyplot as plt
from tqdm import tqdm
import threading as threading
import plotly.express as px
import numpy as np

#def num trade in 

st.title('اینجا میتونی هیستوری سیگنال ها رو اپلود کنی')
 
  

@st.cache_data(ttl='1h' , max_entries=2 )
def convert(dfe):
    con_to_hist = pd.DataFrame()

    for dff in dfe:  
        dff = str(dff)
        if dff in st.session_state :
            df = st.session_state[dff]
            def init_balance(df):
                for index , row in  df.iterrows():
                    if row['Unnamed: 3'] == 'balance':
                        bal =   df.at[index , 'Unnamed: 11']
                        tim =   df.at[index , 'Strategy Tester Report']  
                        break
                if bal and tim :
                    return bal , tim
                else:
                    print('file colume not normal and rejact!!!')
            def create_df(df):
                selected_rows = df[~df['Unnamed: 4'].isin(['in', 'out'])]
                # حذف ردیف‌های انتخاب شده و ایجاد DataFrame جدید
                df = df.drop(selected_rows.index)
                return df
            def col_name(df):
                col = ['Time','Deal','Symbol','Type','Direction','Volume','Price','Order','Commission','Swap','Profit','Balance','Comment']
                
                df.columns = col
                return df
            def to_date_time(df):
                df['Time'] = pd.to_datetime(df['Time'], format='%Y.%m.%d %H:%M:%S')
                return df    
            def ea_to_signal(df, a_one, a_one_two):
                df.reset_index(drop=True, inplace=True)
                newdf = pd.DataFrame({'Type': ['Balance'] , 'Profit': [a_one] , 'Time': [a_one_two]})
                newdf = pd.concat([newdf, pd.DataFrame({'Type': 'Balance', 'Profit': a_one , 'Time': a_one_two}, index=[0])], ignore_index=True)
                non = True
                for index , row in df.iterrows():
                    if index > 0 :
                        if row['Type'] == 'balance' :

                            newdf.at[index , 'Price'] =   df.at[index , 'Unnamed: 11']
                            newdf.at[index , 'Time'] =   df.at[index , 'Strategy Tester Report']
                            non = False  
                            continue


                        elif row['Direction'] == 'in':
                            newdf.at[index , 'Time']         = df.at[index, 'Time']
                            newdf.at[index , 'Symbol']       = df.at[index, 'Symbol']
                            newdf.at[index , 'Type']         = df.at[index, 'Type']
                            newdf.at[index , 'Volume']       = df.at[index, 'Volume']
                            newdf.at[index , 'Price']        = df.at[index, 'Price']
                            newdf.at[index , 'Commission']   = df.at[index, 'Commission']
                            newdf.at[index , 'Swap']         = df.at[index, 'Swap']
                            newdf.at[index , 'Balance_now']  = df.at[index, 'Balance']
                            newdf.at[index , 'Comment']      = df.at[index, 'Comment']   
                        elif row['Direction'] == 'out':
                            indexx = index-1
                            newdf.at[indexx , 'Profit']      = df.at[index, 'Profit']
                            newdf.at[indexx , 'Time_1']      = df.at[index, 'Time']
                            newdf.at[indexx , 'Price_1']     = df.at[index, 'Price']
                            newdf.at[indexx , 'Balance_now'] = df.at[index, 'Balance']
                    
                newdf.iloc[[1,0],:] = newdf.iloc[[0,1],:]
                newdf.reset_index(drop=True, inplace=True)
                df = newdf.drop(newdf[(newdf['Type'] == 'Balance') & newdf['Price_1'].notna()].index)
                #newdff = newdf.replace(',', ';', regex=True)
                return df

            a_one , a_one_two = init_balance(df)
            a_two = create_df(df)
            a_tre = col_name(a_two)
            a_for = to_date_time(a_tre)
            a_five= ea_to_signal(a_for, a_one , a_one_two)
            #a_five.iloc[0] = a_five.iloc[0].fillna('')
            
            a_five = a_five.iloc[::-1]
            
            #a_five.to_csv('nana.csv', mode='w', index = False)
            
            #st.write(a_five.columns)
            con_to_hist = pd.concat([con_to_hist, a_five], ignore_index=True)
            del st.session_state[dff]
    #st.session_state.con_to_hist = con_to_hist
    return con_to_hist

@st.cache_data(ttl='1h' , max_entries=2 )
def analhist_two(file_list):



    #st.write(file_list)
    hist_tow = pd.DataFrame()
    try:
        
        df = file_list
        df = df[::-1].reset_index(drop=True)
        

        df['Type'] = df['Type'].str.capitalize()
        
        df['Time']    = pd.to_datetime(df['Time'])
        df['Time_1']  = pd.to_datetime(df['Time_1'])
        df['Profit']  = df['Profit'].astype(str).str.replace(' ', '')
        df['Profit']  = pd.to_numeric(df['Profit'].str.replace(' ', ''), errors='coerce')
        df['Price_1'] = df['Price_1'].astype(str).str.replace(' ', '')
        df['Price_1'] = pd.to_numeric(df['Price_1'].str.replace(' ', ''), errors='coerce')
        df['Price']   = df['Price'].astype(str).str.replace(' ', '')
        df['Price']   = pd.to_numeric(df['Price'].str.replace(' ', ''), errors='coerce')
        df['Volume']  = pd.to_numeric(df['Volume'], errors='coerce')
        df['name']    = None
        num = 0
        num2 = 0
        balance = 0
        a = 0
        column_names = df.columns.tolist()

        # یا به صورت مستقیم
        # column_names = list(df.columns)

        # نمایش نام‌های ستون‌ها
        print(column_names)
        for index, row in df.iterrows():
            #print(row)
            a = a+1
            if row['Type'] != 'Balance' and num2 == 0:
                num = num + 1
                st.write(f'ریپورت ربات شما بالانس ابتدایی ندارد')
                break

            if row['Type'] == 'Balance':

                balance = row['Profit']
                num2 = num2 + 1
                df = df.drop(index)
                print(f'task init balance {balance}')
                continue

            if num2 != 0:
                if row['Type'] not in ['Buy', 'Sell']:
                    #print(f'task problm in tpye row {row}')
                    df = df.drop(index)
                    
                    continue
                balance = balance + df.at[index , 'Profit']                    
                df.at[index, 'balance']                = balance
                df.at[index, 'ABSPP']                  = abs(row['Profit'] * 100) / balance
                df.at[index, 'PP']                     = (row['Profit'] * 100) / balance
                
                if (row['Time_1'] - row['Time']).total_seconds() > 0 :
                    df.at[index, 'deltaH'] = (row['Time_1'] - row['Time']).total_seconds() / 3600
                    df.at[index, 'deltaM'] = (row['Time_1'] - row['Time']).total_seconds() / 60
                else:
                    df.at[index, 'delta'] = 1 


                df.at[index, 'ABSpipeg']               = abs(row['Price_1'] - row['Price']) * 1000
                df.at[index, 'V/B']                    = (row['Volume'] * 100000) / balance

                if row['Price_1'] - row['Price'] == 0:
                    df.at[index, 'ABSpipeg'] = 0

                if row['Price_1'] - row['Price'] > 0 :
                    if row['Type'] == 'Buy':
                        df.at[index, '+pipeg']          = row['Price_1'] - row['Price'] * 1000            
                        df.at[index, '+pipeg/deltaH']   = df.at[index, '+pipeg'] / df.at[index, 'deltaH']
                        df.at[index, '+pipeg/deltaM']   = df.at[index, '+pipeg'] / df.at[index, 'deltaM']
                        df.at[index, '+pipeg/Balance']  = df.at[index, '+pipeg'] / balance
                        df.at[index, '+pipeg/VB']       = df.at[index, '+pipeg'] / df.at[index, 'V/B']
                        

                    if row['Type'] == 'Sell':
                        df.at[index, '-pipeg']          = row['Price_1'] - row['Price'] * 1000
                        df.at[index, '-pipeg/deltaH']   = df.at[index, '-pipeg'] / df.at[index, 'deltaH']
                        df.at[index, '-pipeg/deltaM']   = df.at[index, '-pipeg'] / df.at[index, 'deltaM']
                        df.at[index, '-pipeg/Balance']  = df.at[index, '-pipeg'] / balance
                        df.at[index, '-pipeg/VB']       = df.at[index, '-pipeg'] / df.at[index, 'V/B']
                if row['Price_1'] - row['Price'] < 0 :
                    if row['Type'] == 'Sell':
                        df.at[index, '+pipeg']          = row['Price_1'] - row['Price'] * 1000            
                        df.at[index, '+pipeg/deltaH']   = df.at[index, '+pipeg'] / df.at[index, 'deltaH']
                        df.at[index, '+pipeg/deltaM']   = df.at[index, '+pipeg'] / df.at[index, 'deltaM']
                        df.at[index, '+pipeg/Balance']  = df.at[index, '+pipeg'] / balance
                        df.at[index, '+pipeg/VB']       = df.at[index, '+pipeg'] / df.at[index, 'V/B']
                    

                    if row['Type'] == 'Buy':
                        df.at[index, '-pipeg']              = row['Price_1'] - row['Price'] * 1000
                        df.at[index, '-pipeg/deltaH']       = df.at[index, '-pipeg'] / df.at[index, 'deltaH']
                        df.at[index, '-pipeg/deltaM']       = df.at[index, '-pipeg'] / df.at[index, 'deltaM']
                        df.at[index, '-pipeg/Balance']      = df.at[index, '-pipeg'] / balance
                        df.at[index, '-pipeg/VB']           = df.at[index, '-pipeg'] / df.at[index, 'V/B']
                if row['Profit'] > 0:
                    df.at[index, '+P']                  = df.at[index, 'Profit']
                    df.at[index, '+PP']                 = abs(df.at[index, '+P'] * 100) / balance
                    df.at[index, '+PPVB']               = df.at[index, '+PP'] / df.at[index, 'V/B']
                    df.at[index, '+PP/deltaH']          = df.at[index, '+PP'] / df.at[index, 'deltaH']
                    df.at[index, '+PP/deltaM']          = df.at[index, '+PP'] / df.at[index, 'deltaM']

                if row['Profit'] < 0:
                    df.at[index, '-P']                  = df.at[index, 'Profit']
                    df.at[index, '-PP']                 = abs(df.at[index, '-P'] * 100) / balance
                    df.at[index, '-PPVB']               = df.at[index, '-PP'] / df.at[index, 'V/B']
                    df.at[index, '-PP/deltaH']          = df.at[index, '-PP'] / df.at[index, 'deltaH']
                    df.at[index, '-PP/deltaM']          = df.at[index, '-PP'] / df.at[index, 'deltaM']
                if row['Profit'] == 0:
                    df.at[index, 'P'] = df.at[index, 'Profit']

                df.at[index, 'ABSPP%VB']               = (df.at[index, 'ABSPP'] * 100) / (df.at[index, 'V/B'])
                df.at[index, 'deltaH/VB']               =  df.at[index, 'deltaH'] / (df.at[index, 'V/B'])
                df.at[index, 'deltaM/VB']               =  df.at[index, 'deltaM'] / (df.at[index, 'V/B'])
                df.at[index, 'ABSPP/deltaH']            =  df.at[index, 'ABSPP'] / df.at[index, 'deltaH']
                df.at[index, 'ABSPP/deltaM']            =  df.at[index, 'ABSPP'] / df.at[index, 'deltaM']
                
        df = df[::-1]
        


        new_columns = ['P', 'T/P', 'S/L']
        default_values = [None, None, None]
        
        df = df.assign(**{col: default for col, default in zip(new_columns, default_values)})
        

            #desired = ['Time','Type','Volume','Symbol','Price','S/L','T/P','Time_1','Price_1','Commission','Swap','Profit','Comment','Time_1','name','balance','ABSPP','PP','deltaH','deltaM','ABSpipeg','V/B','-pipeg','-pipeg/deltaH','-pipeg/deltaM','-pipeg/Balance','-pipeg/VB','-P','-PP','-PPVB','-PP/deltaH','-PP/deltaM','ABSPP%VB','deltaH/VB','deltaM/VB','ABSPP/deltaH','ABSPP/deltaM','+P','+PP','+PPVB','+PP/deltaH','+PP/deltaM','+pipeg','+pipeg/deltaH','+pipeg/deltaM','+pipeg/Balance','+pipeg/VB','P']
            
            #df.to_csv('data.csv', mode='a', index=False, header=False)
        
        hist_tow = pd.concat([hist_tow, df], ignore_index=True)
        
        st.session_state.analhist_two = hist_tow
        return hist_tow
    except ValueError as er:
        (f'error {er} in analhsit_two')


@st.cache_data(ttl='1h' , max_entries=2 )
def analhist(file_list):
    hist = pd.DataFrame()
    try:
        for a in file_list:
            a = str(a)
            if a in st.session_state:
                df = st.session_state[a]
                df            = df[::-1]
                df['Time']    = pd.to_datetime(df['Time'])
                df['Time_1']  = pd.to_datetime(df['Time.1'])
                df            = df.rename(columns={'Price.1': 'Price_1'})
                df['Profit']  = df['Profit'].astype(str).str.replace(' ', '')
                df['Profit']  = pd.to_numeric(df['Profit'].str.replace(' ', ''), errors='coerce')
                df['Price_1'] = df['Price_1'].astype(str).str.replace(' ', '')
                df['Price_1'] = pd.to_numeric(df['Price_1'].str.replace(' ', ''), errors='coerce')
                df['Price']   = df['Price'].astype(str).str.replace(' ', '')
                df['Price']   = pd.to_numeric(df['Price'].str.replace(' ', ''), errors='coerce')
                df['name']    = str(a)
                num = 0
                num2 = 0
                balance = 0
                a = 0
                for index, row in df.iterrows():
                    a = a+1
                    if row['Type'] != 'Balance' and num2 == 0:
                        num = num + 1
                        print(f'bog for {a} csv ; no balance start and remove')
                        break

                    if row['Type'] == 'Balance':

                        balance = row['Profit']
                        num2 = num2 + 1
                        df = df.drop(index)
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
                            df.at[index, 'deltaH'] = (row['Time_1'] - row['Time']).total_seconds() / 3600
                            df.at[index, 'deltaM'] = (row['Time_1'] - row['Time']).total_seconds() / 60
                        else:
                            df.at[index, 'delta'] = 1 


                        df.at[index, 'ABSpipeg']               = abs(row['Price_1'] - row['Price']) * 1000
                        df.at[index, 'V/B']                    = (row['Volume'] * 100000) / balance

                        if row['Price_1'] - row['Price'] == 0:
                            df.at[index, 'ABSpipeg'] = 0

                        if row['Price_1'] - row['Price'] > 0 :
                            if row['Type'] == 'Buy':
                                df.at[index, '+pipeg']          = row['Price_1'] - row['Price'] * 1000            
                                df.at[index, '+pipeg/deltaH']   = df.at[index, '+pipeg'] / df.at[index, 'deltaH']
                                df.at[index, '+pipeg/deltaM']   = df.at[index, '+pipeg'] / df.at[index, 'deltaM']
                                df.at[index, '+pipeg/Balance']  = df.at[index, '+pipeg'] / balance
                                df.at[index, '+pipeg/VB']       = df.at[index, '+pipeg'] / df.at[index, 'V/B']
                                

                            if row['Type'] == 'Sell':
                                df.at[index, '-pipeg']          = row['Price_1'] - row['Price'] * 1000
                                df.at[index, '-pipeg/deltaH']   = df.at[index, '-pipeg'] / df.at[index, 'deltaH']
                                df.at[index, '-pipeg/deltaM']   = df.at[index, '-pipeg'] / df.at[index, 'deltaM']
                                df.at[index, '-pipeg/Balance']  = df.at[index, '-pipeg'] / balance
                                df.at[index, '-pipeg/VB']       = df.at[index, '-pipeg'] / df.at[index, 'V/B']
                        if row['Price_1'] - row['Price'] < 0 :
                            if row['Type'] == 'Sell':
                                df.at[index, '+pipeg']          = row['Price_1'] - row['Price'] * 1000            
                                df.at[index, '+pipeg/deltaH']   = df.at[index, '+pipeg'] / df.at[index, 'deltaH']
                                df.at[index, '+pipeg/deltaM']   = df.at[index, '+pipeg'] / df.at[index, 'deltaM']
                                df.at[index, '+pipeg/Balance']  = df.at[index, '+pipeg'] / balance
                                df.at[index, '+pipeg/VB']       = df.at[index, '+pipeg'] / df.at[index, 'V/B']
                            

                            if row['Type'] == 'Buy':
                                df.at[index, '-pipeg']              = row['Price_1'] - row['Price'] * 1000
                                df.at[index, '-pipeg/deltaH']       = df.at[index, '-pipeg'] / df.at[index, 'deltaH']
                                df.at[index, '-pipeg/deltaM']       = df.at[index, '-pipeg'] / df.at[index, 'deltaM']
                                df.at[index, '-pipeg/Balance']      = df.at[index, '-pipeg'] / balance
                                df.at[index, '-pipeg/VB']           = df.at[index, '-pipeg'] / df.at[index, 'V/B']

                        if row['Profit'] > 0:
                            df.at[index, '+P']                  = df.at[index, 'Profit']
                            df.at[index, '+PP']                 = abs(df.at[index, '+P'] * 100) / balance
                            df.at[index, '+PPVB']               = df.at[index, '+PP'] / df.at[index, 'V/B']
                            df.at[index, '+PP/deltaH']          = df.at[index, '+PP'] / df.at[index, 'deltaH']
                            df.at[index, '+PP/deltaM']          = df.at[index, '+PP'] / df.at[index, 'deltaM']

                        if row['Profit'] < 0:
                            df.at[index, '-P']                  = df.at[index, 'Profit']
                            df.at[index, '-PP']                 = abs(df.at[index, '-P'] * 100) / balance
                            df.at[index, '-PPVB']               = df.at[index, '-PP'] / df.at[index, 'V/B']
                            df.at[index, '-PP/deltaH']          = df.at[index, '-PP'] / df.at[index, 'deltaH']
                            df.at[index, '-PP/deltaM']          = df.at[index, '-PP'] / df.at[index, 'deltaM']

                        if row['Profit'] == 0:
                            df.at[index, 'P'] = df.at[index, 'Profit']

                        df.at[index, 'ABSPP%VB']                = (df.at[index, 'ABSPP'] * 100) / (df.at[index, 'V/B'])
                        df.at[index, 'deltaH/VB']               =  df.at[index, 'deltaH'] / (df.at[index, 'V/B'])
                        df.at[index, 'deltaM/VB']               =  df.at[index, 'deltaM'] / (df.at[index, 'V/B'])
                        df.at[index, 'ABSPP/deltaH']            =  df.at[index, 'ABSPP'] / df.at[index, 'deltaH']
                        df.at[index, 'ABSPP/deltaM']            =  df.at[index, 'ABSPP'] / df.at[index, 'deltaM']
                        
                df = df[::-1]
                #if not os.path.exists('data.csv'):
                #    df.to_csv('data.csv', mode='w', index=False)
                    
                #else:
                #    df.to_csv('data.csv', mode='a', index=False, header=False)
                
                hist = pd.concat([hist, df], ignore_index=True)
            if a in st.session_state:
                del st.session_state[a]   
        
        st.session_state.analhist = hist
        
        return hist
            
    except ValueError as er:
        st.write(f'erorr in {er} func')

@st.cache_data(ttl='1h', max_entries=2, experimental_allow_widgets=True)
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

        return filtered_df


def inside(df):

    for index, row in df.iterrows():
        df.at[index,'ABSPP']                = abs(row['Profit'] * 100) / df.at[index,'balance']
        df.at[index,'PP']                   =    (row['Profit'] * 100) / df.at[index,'balance']
        df.at[index,'V/B']                  =    (row['Volume'] * 100000) / df.at[index,'balance']
                                                
        df.at[index,'+pipeg/Balance']        =    row['+pipeg'] / df.at[index,'balance']
        df.at[index,'+pipeg/VB']             =    row['+pipeg'] / df.at[index,'V/B']
        
        df.at[index,'-pipeg/Balance']        =    row['-pipeg'] / df.at[index,'balance']
        df.at[index,'-pipeg/VB']             =    row['-pipeg'] / df.at[index,'V/B']

        df.at[index,'+PP']                  = abs(row['+P'] * 100) / df.at[index,'balance']
        df.at[index,'+PPVB']                 =    row['+PP'] / df.at[index,'V/B']
        df.at[index,'+PP/deltaH']             =   row['+PP'] / df.at[index,'deltaH']
        df.at[index,'+PP/deltaM']             =   row['+PP'] / df.at[index,'deltaM']

        df.at[index,'-PP']                  = abs(row['-P'] * 100) / df.at[index,'balance']
        df.at[index,'-PPVB']                 =    row['-PP'] / df.at[index,'V/B']
        df.at[index,'-PP/deltaH']             =   row['-PP'] / df.at[index,'deltaH']
        df.at[index,'-PP/deltaM']             =   row['-PP'] / df.at[index,'deltaM']

        df.at[index,'ABSPP%VB']               = (row['ABSPP'] * 100) / (df.at[index,'V/B'])
        df.at[index,'deltaH/VB']               =  row['deltaH'] / (df.at[index,'V/B'])
        df.at[index,'deltaM/VB']               =  row['deltaM'] / (df.at[index,'V/B'])
        df.at[index,'ABSPP/deltaH']            =  row['ABSPP'] / df.at[index,'deltaH']
        df.at[index,'ABSPP/deltaM']            =  row['ABSPP'] / df.at[index,'deltaM']


    return df


def mainchart(df): #timePPm()
    win        = (df['Profit'] > 0).sum()
    loss       = (df['Profit'] < 0).sum()
    winrate    = (win * 100) / (win + loss)
    trades     = len(df)
    besttrade  = df['PP'].max()
    worsttrade = df['PP'].min()
    avgtimetrade = df['deltaM'].mean()
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
        st.metric("میانگین سود به درصد", f"{avgProfit:.2f}")
        st.metric("میانگین زمان به دقیقه", f"{avgtimetrade:.2f}")
    
    # ستون دوم
    with col2:
        st.metric("بهترین معامله", f"{besttrade:.2f}%")
        st.metric("بدترین معامله", f"{worsttrade:.2f}%")  
        st.metric("میانگین ضرر به درصد", f"{avgLoss:.2f}%")
        st.metric("میانگین حجم به موجودی", f"{avgVB:.2f}")

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
    
    labels = 'win trade','loss trade' 
    sizes = [win, loss]
    explode = (0, 0.2)  # only "explode" the 2nd slice (i.e. 'Hogs')
    colors = ['green', 'red']

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90, colors=colors)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)
    # نمایش دیتافریم   
    st.dataframe(df.head())


def p_chart_one(df):

    # ایجاد یک دیتافریم خالی برای ذخیره میانگین PP برای هر نماد و نوع تراکنش
    average_pp_df = pd.DataFrame(columns=['Symbol', 'Type', 'Average Positive PP', 'Average Negative PP'])

    # حلقه برای محاسبه میانگین PP برای تمام نمادها و انواع تراکنش‌ها
    symbols = df['Symbol'].unique()
    types = df['Type'].unique()

    for symbol in symbols:
        for type in types:
            filtered_df = df[(df['Symbol'] == symbol) & (df['Type'] == type)]
            average_positive_pp = filtered_df[filtered_df['PP'] > 0]['PP'].mean()
            average_negative_pp = filtered_df[filtered_df['PP'] < 0]['PP'].mean()
            # افزودن به دیتافریم با استفاده از دستور loc
            average_pp_df.loc[len(average_pp_df)] = [symbol, type, average_positive_pp, average_negative_pp]

    # ایجاد نمودار با استفاده از کتابخانه Plotly
    fig = px.bar(average_pp_df, x='Symbol', y=['Average Positive PP', 'Average Negative PP'],
                title='Average PP by Symbol and Type (Positive and Negative)',
                labels={'Symbol': 'Symbol (Type)', 'variable': 'PP Type', 'value': 'Average PP'})
    fig.update_layout(barmode='group')

    # نمایش نمودار با استفاده از Streamlit
    st.plotly_chart(fig, width=0, height=700)

    
def p_chart_two(df):

    # ایجاد یک دیتافریم خالی برای ذخیره میانگین PP برای هر نماد و نوع تراکنش
    average_pp_df = pd.DataFrame(columns=['Symbol', 'Type', 'Average Positive PP', 'Average Negative PP'])

    # حلقه برای محاسبه میانگین PP برای تمام نمادها و انواع تراکنش‌ها
    symbols = df['Symbol'].unique()
    types = df['Type'].unique()

    for symbol in symbols:
        for type in types:
            filtered_df = df[(df['Symbol'] == symbol) & (df['Type'] == type)]
            average_positive_pp = filtered_df[filtered_df['PP'] > 0]['PP'].sum()
            average_negative_pp = filtered_df[filtered_df['PP'] < 0]['PP'].sum()
            # افزودن به دیتافریم با استفاده از دستور loc
            average_pp_df.loc[len(average_pp_df)] = [symbol, type, average_positive_pp, average_negative_pp]

    # ایجاد چارت میله‌ای با میانگین PP مثبت و منفی با رنگ‌های متفاوت با Matplotlib
    fig, ax = plt.subplots()
    bar_width = 0.35
    bar_positions = range(len(average_pp_df))
    bar1 = ax.bar(bar_positions, average_pp_df['Average Positive PP'], width=bar_width, label='Positive PP', color='g')
    bar2 = ax.bar([pos + bar_width for pos in bar_positions], average_pp_df['Average Negative PP'], width=bar_width, label='Negative PP', color='r')

    ax.set_xlabel('Symbol')
    ax.set_ylabel('PP')
    ax.set_title('Average PP by Symbol and Type (Positive and Negative)')
    ax.set_xticks([pos + bar_width / 2 for pos in bar_positions])
    #ax.set_xticklabels(average_pp_df.apply(lambda row: f"{row['Symbol']}", axis=1))
    ax.set_xticklabels(average_pp_df.apply(lambda row: f"{row['Symbol']} ({row['Type']})", axis=1), rotation=90)

    ax.legend()

    # نمایش نمودار با استفاده از Streamlit
    st.pyplot(fig)


def time_chart(df):
    st.write('نمایش چارت دقیقه')
    st.line_chart(df, x='Time', y='deltaM', width=0, height=700)

    st.write('نمایش چارت ساعت')
    st.line_chart(df, x='Time', y='deltaH', width=0, height=700)
        
        
def p_chart(df):
    st.title('نمودار تایپ معاملات ')

    result = df.groupby(['Symbol', 'Type']).size().unstack(fill_value=0)

    # اضافه کردن نتایج به دیتافریم اصلی به صورت افقی
    df = df.join(result, on='Symbol', rsuffix='_count')
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset=['Symbol'])
    st.bar_chart(df,x='Symbol', y =['Buy', 'Sell'] , width=0, height=700 )
    pass


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

    result = df.groupby(['Symbol', 'deltaH']).size().unstack(fill_value=0)

    # اضافه کردن نتایج به دیتافریم اصلی به صورت افقی
    df = df.join(result, on='Symbol', rsuffix='_count')
    

    df = df.drop_duplicates()
    df['Hdelta'] = df['deltaH']
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
    st.line_chart(df , x = 'Time' , y= 'cospp' ,  width=800, height=700)





    colorscale = [[0, 'rgb(255,0,0)'], [0.5, 'rgb(255,255,0)'], [1, 'rgb(0,128,0)']] 
    fige = px.scatter(df, x='V/B', y='PP' )
    fige.update_traces(
        marker = dict(
            color = np.select([df['PP']<0, df['PP']>0], 
                            [df['PP'], df['PP']], 0),
            colorscale = colorscale,
            showscale = True
        )
    )
    fige.update_layout(width=800, height=1100)
    #fige.update_traces(marker=dict(size=2))
    st.plotly_chart(fige)






    colorscale = [[0, 'rgb(255,0,0)'], [0.5, 'rgb(255,255,0)'], [1, 'rgb(0,128,0)']] 
    figen = px.scatter(df, x='Time', y='PP' )
    figen.update_traces(
        marker = dict(
            color = np.select([df['PP']<0, df['PP']>0], 
                            [df['PP'], df['PP']], 0),
            colorscale = colorscale,
            showscale = True
        )
    )
    figen.update_layout(width=800, height=1100)
    #fige.update_traces(marker=dict(size=2))
    st.plotly_chart(figen)





    st.write('نمودار تایم پوزیشن و پیپیچ')

    fifo = px.line(df , x = 'Time' , y= 'ABSpipeg' ,  width=800, height=800)


    st.plotly_chart(fifo)

    pip_va = px.scatter(df , x='PP' , y = 'ABSpipeg')
    pip_va.update_layout(width=800, height=1100)
    st.plotly_chart(pip_va)



    pip_v = px.scatter(df , x='V/B' , y = 'ABSpipeg')
    pip_v.update_layout(width=800, height=1100)
    st.plotly_chart(pip_v)

    pip_vv = px.scatter(df , x='deltaM' , y = 'ABSpipeg')
    pip_vv.update_layout(width=800, height=1100)
    st.plotly_chart(pip_vv)






    dfr = df
    dfr.fillna(0, inplace=True)

    p = dfr['-PP']
    p = -p

    fig = px.line(dfr, x='Time', y=['+PP', p], 
                color_discrete_map={'Column1': 'green', 'Column2': 'red'},
                template='presentation',  width=900, height=750 , line_shape='hv')


    fig.update_traces(line=dict(width=2))
    st.plotly_chart(fig)







    dfs = df
    dfs.fillna(0, inplace=True)
    ps = dfs['-PP'].cumsum()
    ps = -ps
    pps = dfs['+PP'].cumsum()

    figs = px.line(dfs, x='Time', y=[pps, ps], 
                color_discrete_map={'Column1': 'green', 'Column2': 'red'},
                template='presentation',  width=900, height=750 , line_shape='hv')

    ys = dfs['PP'].cumsum()
    new_line = px.line(dfs, x='Time', y= ys , color_discrete_sequence=['blue']).data[0]
    figs.add_trace(new_line)

    # تنظیمات بیشتر
    figs.update_layout(title='My Plot')
    figs.update_xaxes(title_text='Time')
    figs.update_traces(line=dict(width=2))
    st.plotly_chart(figs)

    psa = dfs['-PP'].cumsum()
    psa = -psa
    ppsa = dfs['+PP'].cumsum()
    ysa = dfs['PP'].cumsum()

    figsf = px.scatter(dfs, x='Time', y=[ppsa, psa , ysa], 
                    color_discrete_map={'ppsa': 'green', 'psa': 'red' , 'ysa' : 'blue'},  
                    template='presentation',  
                    width=900, height=750)

 
    figsf.update_traces(marker_size=4) 
    figsf.data[0].marker.color = 'green'  
    figsf.data[1].marker.color = 'red'  
    figsf.data[2].marker.color = 'blue'  
    figsf.update_layout(title='My Plot')
    figsf.update_xaxes(title_text='Time') 

    st.plotly_chart(figsf)







    size_min = 1  # حداقل اندازه نقاط
    size_max = 2 # حداکثر اندازه نقاط

    # نگاشت مقادیر PP به بازه اندازه‌ها
    df['point_size'] = 1 #df['PP'].apply(lambda x: size_min + (size_max - size_min) * (x - df['PP'].min()) / (df['PP'].max() - df['PP'].min()))

    # ساخت نمودار با اندازه‌های متغیر برای نقاط
    fig = px.scatter_3d(df, x='PP', y='V/B', z='deltaM', color='PP', 
                        color_continuous_scale='RdYlGn', size='2')
    fig.update_layout(width=800, height=1100)

    # تنظیم نمودار رنگی
    fig.update_coloraxes(colorbar_title='PP', cmin=df['PP'].min(), cmax=df['PP'].max())

    st.plotly_chart(fig)

    #@st.cache_data(ttl='1h', max_entries=2, experimental_allow_widgets=True)

    #def اتو اسکیل ایجاد


def pp4_chart(df):

    colorscale = [[0, 'rgb(255,0,0)'], [0.5, 'rgb(255,255,0)'], [1, 'rgb(0,128,0)']]

    # داده‌های دیگر برای نمودار سوم (خطی)
    dfr = df.copy()
    dfr.fillna(0, inplace=True)
    p = -dfr['-PP']

    # ایجاد یک چارت ترکیبی
    fig = go.Figure()

    # اضافه کردن نمودار خطی (line)
    fig.add_trace(go.Scatter(x=dfr['Time'], y=dfr['+PP'], line=dict(color='green'), name='خط 1 (سبز)'))

    # اضافه کردن نمودار scatter
    fig.add_trace(go.Scatter(x=dfr['Time'], y=p, mode='markers', marker=dict(
        color=df['PP'],
        colorscale=colorscale,
        size=8,
        showscale=True
    ), name='خط 2 (قرمز)'))

    fig.update_layout(
        template='presentation',
        width=900,
        height=750
    )
    fig.update_traces(line=dict(width=2))

    # نمایش چارت ترکیبی در Streamlit
    st.plotly_chart(fig)


def Dchart(df,x_col,y_col,z_col):

    
    if x_col and y_col :

        fig_line = px.line(df , x=x_col, y=y_col )
        fig_line.update_layout(width=700, height=1000)
        fig_line.update_traces(marker=dict(size=2))
        st.plotly_chart(fig_line)

        fig_2d = px.scatter(df, x=x_col, y=y_col)
        fig_2d.update_layout(width=700, height=1000)
        fig_2d.update_traces(marker=dict(size=2))
        st.plotly_chart(fig_2d)


    if z_col:
        fig_3d = px.scatter_3d(df, x=x_col, y=y_col, z=z_col)
        fig_3d.update_layout(width=700, height=1000)
        fig_3d.update_traces(marker=dict(size=2))
        st.plotly_chart(fig_3d)


def pl_chart(df):

    df.fillna(0, inplace=True)
    p = df['-PP']
    p = -p
    fig = px.line(df, x='Time', y=['+PP', p], 
                color_discrete_map={'Column1': 'green', 'Column2': 'red'},
                template='simple_white', width=800, height=700)

    fig.update_traces(line=dict(width=2))

    st.plotly_chart(fig)


def main_chart_one(df):
    # چارت حجم بر زمان         چارت تعداد معاملات باز بر زمان 
    df['Volume'] = df['Volume'].astype(float)
    df['Time']    = pd.to_datetime(df['Time'])
    if 'Time.1' in df.columns:
        df['Time_1']  = pd.to_datetime(df['Time.1'])
    else:
        df['Time_1']  = pd.to_datetime(df['Time_1'])
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

@st.cache_data(ttl='1h' , max_entries=2 )
def main_change(df, selected_symbols,selected_symbols_two):

    # حذف نماد 
    
    
    
    df_copy = df.copy()
    
    
    df_copy = df_copy[~df_copy['Symbol'].isin(selected_symbols)]
    
    
    st.write("دیتافریم پس از حذف:")
    df = df_copy
    df = df.rename(columns={'+P': 'temp1', 
                            '+PP': 'temp2',
                            '-P': 'temp3',
                            '-PP': 'temp4'})

    df = df.rename(columns={'temp1': '-P', 
                            'temp2': '-PP', 
                            'temp3': '+P',
                            'temp4': '+PP'})




    # تغییر مقادیر مطابق با انتخاب کاربر
    for symbol in selected_symbols_two:
        # تغییر مقادیر ستون Type
        # تبدیل 'Sell' به 'Buy' و برعکس
        df['Type'] = df['Type'].map({'Sell': 'Buy', 'Buy': 'Sell'})


        # معکوس کردن مقادیر ستون Profit
        df.loc[df['Symbol'] == symbol, 'Profit'] = -df.loc[df['Symbol'] == symbol, 'Profit']
        df.loc[df['Symbol'] == symbol, 'PP'] = -df.loc[df['Symbol'] == symbol, 'PP']
    
     

    
    intbalance = 0
    z_row = 0
    
    mybar = st.progress(0)
    num_prog_init = int(len(df)/100)
    st.session_state.num_prog = -1
    prog_num = 0
    for index, row in df.iterrows():
        if prog_num == num_prog_init:
            st.session_state.num_prog  += 1
            # به‌روزرسانی مقدار متغیر progress bar
            val = st.session_state.num_prog
            if val < 101:
                mybar.progress(val)
            
            #st.write(prog_num , num_prog_init , val)
            prog_num = 0
        prog_num = prog_num + 1
        if z_row == 0 :
            df.at[index , 'balance'] = df.at[index , 'balance'] + df.at[index , 'Profit'] 
            intbalance = df.at[index , 'balance']
        else:
            df.at[index , 'balance'] = intbalance + df.at[index , 'Profit']
            intbalance = df.at[index , 'balance']
    del st.session_state.num_prog

            
    # نمایش دیتافریم تغییر یافته
    df
    st.session_state.data_tow = df


    # فیلتر زمان معاملات 



def main_app():

    uploaded_files = st.file_uploader("هیستوری ها رو انتخاب کن", accept_multiple_files=True, type=['csv'] , key= 'up_one')
    uploaded_filess = st.file_uploader("هیستوری ها رو انتخاب کن", accept_multiple_files=True , type=['xlsx'], key= 'up_two')



    file_paths = []
    file_pathss = []




    if uploaded_files  or uploaded_filess :


        for file in uploaded_files: 
            df = pd.read_csv(io.StringIO(file.read().decode('utf-8')) , delimiter=';') 
            df
            file_name = file.name
            file_path = file.name 
            file_paths.append(file_path)
            session_his = str(file_name)
            st.session_state[session_his] = df
            
            #df.to_csv(file_name ,sep = ';', index=False )
            # دسترسی به لیست آدرس فایل ها
        

        for filee in uploaded_filess: 
            #df = pd.read_excel(io.StringIO(file.read().decode('utf-8')))
            df_rep = pd.read_excel(filee)
            df_rep
            file_nameee = filee.name
            file_pathh = filee.name 
            file_pathss.append(file_pathh)
            session_rep = str(file_nameee)
            st.session_state[session_rep] = df_rep
            #st.session_state[f'{file.namee}'] = dfd
            #file_namee = os.path.splitext(file.name)[0] + '.csv'
            #df.to_excel(file_namee, index=False )
            # دسترسی به لیست آدرس فایل ها





        st.title('انتخاب فایل های مورد نظر برای انجام پردازش ')

        selected_files = st.multiselect(' سیگنال ها  ', uploaded_files , key= 'selc_one')
        selected_filess = st.multiselect('ریپورت های ربات ', uploaded_filess , key = 'selc_two')

        filelist = []
        filelistt = []



        
        if st.button('پردازش روی فایل های انتخاب شده'):
            if 'analhist' in st.session_state:
                del st.session_state['analhist']
            if 'analhist_two' in st.session_state:
                del st.session_state['analhist_two']                
            if 'data_tow' in st.session_state:
                del st.session_state['data_tow']

            for file in selected_files:
                st.write(f'name file : {file.name}','.....', f'size : {file.size}k')
                filelist.append(file.name)
                #st.session_state.history = file.name
            for filee in selected_filess:
                st.write(f'name file : {filee.name}','.....', f'size : {filee.size}k')
                #filename = os.path.splitext(filee.name)[0] + '.csv'
                filename = filee.name
                filelistt.append(filename)
                #st.session_state.report = filee.name       
                # نام فایل برای پاک کردن


            
            if len(filelist) > 0 and len(filelistt) == 0 :
                analhist(filelist)
            if len(filelist) > 0 and len(filelistt) > 0 :
                analhist(filelist)

                file_convert = convert(filelistt)
                analhist_two(file_convert)


            if len(filelist) == 0 and len(filelistt) > 0 :
                file_convert = convert(filelistt)
                analhist_two(file_convert)

main_app()





if 'analhist' in st.session_state or 'analhist_two' in st.session_state :


    if 'analhist' in st.session_state and 'analhist_two' in st.session_state :
        df1 = st.session_state.analhist
        df2 = st.session_state.analhist_two

    # ترکیب دو دیتافریم
        dffg = pd.concat([df1, df2])

    else:

        if 'analhist' in st.session_state: 
            dffg = st.session_state.analhist

        if 'analhist_two' in st.session_state:

            dffg = st.session_state.analhist_two



    # بازسازی ستون index
        
    



    dffg = dffg.sort_values(by='Time')
    dffg = dffg.reset_index(drop=True)
    
    b =timePPm(dffg)
    d = inside(b)
    d = d[d['deltaM'] <= 600]
    d
    


    if st.button('اطلاعات اماری ' , key = 'anal' ):
        mainchart(d)

    if st.button('چارت های پیشنهادی ' , key = 'anal5' ):
        pp3_chart(d)
    x_col = st.selectbox('Select X column', d.columns, key= 'x_col')
    y_col = st.selectbox('Select Y column', d.columns, key = 'y_col')
    z_col = st.selectbox('Select Z column (optional)', d.columns, key= 'z_col')




    if st.button('ساخت نمودار دلخواه دو بعدی و سه بعدی' , key = 'Dchart'):
        Dchart(d,x_col,y_col,z_col)

    if st.button('لاین چرات مدت زمان معاملات ', key = 'time_chart_one'):
        time_chart(d)


    if st.button('بار چارت معاملات ' , key = 'anal1' ): 
        p_chart(d)


    if st.button('بار چارت سود ضرر هر تایپ در هر نماد ' , key = 'anal1_1' ): 

        p_chart_two(d)

    if st.button('سود ضرر درصدی هر نماد ' , key = 'anal2' ):
        pp_chart(d)
    
    if st.button('مجموع مدت زمان معامله هر نماد ' , key = 'anal3' ):
        pp1_chart(d)


    if st.button('نسبت حجم معامله به موجودی برای هر نماد ' , key = 'anal4' ):
        pp2_chart(d)



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
        main_change(d, selected_symbols,selected_symbols_two)




if 'data_tow' in st.session_state:
    st.header('انجام فرایندهای تحلیل رو دیتافرم شخصی سازی شده ')
    dfff = st.session_state['data_tow']
    bb =timePPm(dfff) 
    dd = inside(bb)
    dd

    if st.button('اطلاعات اماری ' , key = 'ass1' ):
        mainchart(dd)


    if st.button('چارت های پیشنهادی ' , key = 'anal5_1' ):
        pp3_chart(dd)



    if st.button('لاین چارت سود درصدی به زمان ' , key = 'ass6' ):
        pp3_chart(dd)


    if st.button('لاین چرات مدت زمان معاملات ', key = 'time_chart_tow'):
        time_chart(dd)

    if st.button('بار چارت معاملات ' , key = 'ass2' ): 

        p_chart(dd)

    if st.button('بار چارت سود ضرر هر تایپ در هر نماد ' , key = 'ass1_1' ): 

        p_chart_two(dd)

    if st.button('سود ضرر درصدی هر نماد ' , key = 'ass3' ):
        pp_chart(dd)
    
    if st.button('مجموع مدت زمان معامله هر نماد ' , key = 'ass4' ):
        pp1_chart(dd)

    if st.button('نسبت حجم معامله به موجودی برای هر نماد ' , key = 'ass5' ):
        pp2_chart(dd)


    if st.button('حجم و معاملات باز بر زمان ' , key = 'ass7' ):
        main_chart_one(dd)
        
    numberr = st.number_input("Insert a number" , key= 'ass_1')
    st.write('The current number is ', numberr)    
    if st.button('چارت سود با عدد دلخواه' , key = 'ass8' ):

        chart_in_b(dd , numberr)




