import pandas as pd
import streamlit as st
from dateutil.parser import parse

df = pd.read_excel(r'C:\Users\delta2794900\Desktop\mahdi_test.xlsx')
df
#st.session_state['df'] = df
#st.session_state

def convert():
    con_to_hist = pd.DataFrame()


    if 'df' in st.session_state :
        df = st.session_state.df
        df
        def init_balance(df):
            for index , row in  df.iterrows():
                if row['Unnamed: 3'] == 'balance':
                    bal =   df.at[index , 'Unnamed: 11']
                    tim =   df.at[index , 'Trade History Report']  
                    break
            if bal and tim :
                return bal , tim
            else:
                print('file colume not normal and rejact!!!')
        def create_df(df):
            selected_rows = df[~df['Unnamed: 4'].isin(['in', 'out'])]
            # حذف ردیف‌های انتخاب شده و ایجاد DataFrame جدید
            df = df.drop(selected_rows.index)
            df
            return df
        def col_name(df):
            col = ['Time', 'Deal','Symbol','Type','Direction','Volume','Price','Order','Commission','fee','Swap','Profit','Balance','Comment']
            
            df.columns = col
            df
            return df
        def to_date_time(df):
            df['Time'] = pd.to_datetime(df['Time'], format='%Y.%m.%d %H:%M:%S')
            return df    
        def ea_to_signal(df, a_one, a_one_two):
            df.reset_index(drop=True, inplace=True)
            newdf = pd.DataFrame({'Type': ['Balance'] , 'Profit': [a_one] , 'Time': [a_one_two]})
            #newdf = pd.concat([newdf, pd.DataFrame({'Type': 'Balance', 'Profit': a_one , 'Time': a_one_two}, index=[0])], ignore_index=True)
            
            for index , row in df.iterrows():

                newdf.at[index , 'Time']         = row['Time']
                newdf.at[index , 'Symbol']       = row['Symbol']
                newdf.at[index , 'Type']         = row['Type']
                newdf.at[index , 'Volume']       = row['Volume']
                newdf.at[index , 'Price']        = row['Price']
                newdf.at[index , 'Commission']   = row['Commission']
                newdf.at[index , 'Swap']         = row['Swap']
                newdf.at[index , 'Comment']      = row['Comment']                           
                newdf.at[index , 'Profit']       = row['Profit']
                newdf.at[index , 'Time_1']       = row['Time_1']
                newdf.at[index , 'Price_1']      = row['Price_1']
                newdf.at[index , 'Price_1']      = row['Price_1']
                newdf.at[index , 'Price_1']      = row['Price_1']
                        
            #newdf.iloc[[1,0],:] = newdf.iloc[[0,1],:]
            newdf.reset_index(drop=True, inplace=True)
            #newdff = newdf.replace(',', ';', regex=True)
            return newdf

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
        con_to_hist
    #st.session_state.con_to_hist = con_to_hist
    return con_to_hist


#def analhist_two(file_list):



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
                if row['Price_1'] - row['Price'] == 0 :
                    df = df.drop(index)
                    continue
                balance = balance + df.at[index , 'Profit']                    
                df.at[index, 'balance']                = balance
                df.at[index, 'ABSPP']                  = abs(row['Profit'] * 100) / balance
                df.at[index, 'PP']                     = (row['Profit'] * 100) / balance
                
                
                df.at[index, 'deltaH'] = (row['Time_1'] - row['Time']).total_seconds() / 3600
                df.at[index, 'deltaM'] = (row['Time_1'] - row['Time']).total_seconds() / 60


                df.at[index, 'ABSpipeg']               = abs(row['Price_1'] - row['Price']) * 1000
                df.at[index, 'V/B']                    = (row['Volume'] * 100000) / balance


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


def analhist_tre(df):
    con_to_hist = pd.DataFrame()

    def init_balance(df):
        for index , row in  df.iterrows():
            if row['Unnamed: 3'] == 'balance':
                bal =   df.at[index , 'Unnamed: 11']
                tim =   df.at[index , 'Trade History Report']  
                break
        if bal and tim :
            return bal , tim
        else:
            print('file colume not normal and rejact!!!')

    def clean(df):
        s = 0
        for index , row in df.iterrows():
            if row['Trade History Report'] == 'Positions':
                index_one = index +2
                st.write(index_one)
                s = s+1
            if row['Trade History Report'] == 'Orders':
                index_two = index
                st.write(index_two)
                s = s +1
            if s == 2:
                
                df = df.drop(df.index[index_two:])
                df = df.loc[index_one:]
            
        df = df.reset_index(drop=True)
        return df

    def col_name(df):
        col = ['Time','Position','Symbol','Type','Volume','Price','S/L','T/P','Time_1','Price_1', 'Commission','Swap','Profit','Comment']
        
        df.columns = col
        df
        return df

    def to_date_time(df):
        df['Time'] = df['Time'].apply(lambda x: parse(x).strftime('%Y.%m.%d %H:%M:%S'))
        df['Time_1'] = df['Time_1'].apply(lambda x: parse(x).strftime('%Y.%m.%d %H:%M:%S'))
        df['Time'] = pd.to_datetime(df['Time'])
        df['Time_1'] = pd.to_datetime(df['Time_1'])
        return df    

    def ea_to_signal(df, a_one, a_one_two):
        df.reset_index(drop=True, inplace=True)
        newdf = pd.DataFrame({'Type': ['Balance'] , 'Profit': [a_one] , 'Time': [a_one_two]})
        #newdf = pd.concat([newdf, pd.DataFrame({'Type': 'Balance', 'Profit': a_one , 'Time': a_one_two}, index=[0])], ignore_index=True)
        
        for index , row in df.iterrows():
            index += 1
            newdf.at[index , 'Time']         = row['Time']
            newdf.at[index , 'Symbol']       = row['Symbol']
            newdf.at[index , 'Type']         = row['Type']
            newdf.at[index , 'Volume']       = row['Volume']
            newdf.at[index , 'Price']        = row['Price']
            newdf.at[index , 'Commission']   = row['Commission']
            newdf.at[index , 'Swap']         = row['Swap']
            newdf.at[index , 'Comment']      = row['Comment']                           
            newdf.at[index , 'Profit']       = row['Profit']
            newdf.at[index , 'Time_1']       = row['Time_1']
            newdf.at[index , 'Price_1']      = row['Price_1']
            newdf.at[index , 'Price_1']      = row['Price_1']
            newdf.at[index , 'Price_1']      = row['Price_1']
                    
        #newdf.iloc[[1,0],:] = newdf.iloc[[0,1],:]
        newdf.reset_index(drop=True, inplace=True)
        #newdff = newdf.replace(',', ';', regex=True)
        return newdf

    a_one , a_one_two = init_balance(df)
    a_two = clean(df)
    a_tre = col_name(a_two)
    a_for = to_date_time(a_tre)
    a_five= ea_to_signal(a_for, a_one , a_one_two)
    #a_five.iloc[0] = a_five.iloc[0].fillna('')
    
    a_five = a_five.iloc[::-1]
    
    #a_five.to_csv('nana.csv', mode='w', index = False)
    
    #st.write(a_five.columns)
    con_to_hist = pd.concat([con_to_hist, a_five], ignore_index=True)
    
    #st.session_state.con_to_hist = con_to_hist
    return con_to_hist

df = analhist_tre(df)

df