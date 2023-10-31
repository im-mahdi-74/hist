
import streamlit as st
import numpy as np
import time
import random
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
import MetaTrader5 as mt5  # pip install MetaTrader5
import time


def one():
    # Create a function to generate random data
    def generate_data():
        # Generate a random number between 0 and 100
        data = np.random.randint(0, 100, size=(100,))
        return data

    # Create a line chart
    chart = st.line_chart(generate_data())

    # Start a loop to continuously generate data and update the chart
    while True:
        # Generate new data
        new_data = generate_data()

        # Update the chart with the new data
        chart.add_rows(new_data)

        # Sleep for 1 second
        time.sleep(1)


def two():
    # Create a function to generate random data
    def generate_data():
        # Generate a random number between 0 and 100
        data = np.random.randint(0, 100, size=(100,))
        return data

    # Create a line chart
    chart = st.line_chart(generate_data())

    # Add a slider to control the update interval
    update_interval = st.slider("Update interval (seconds)", 1, 10, 1)

    # Start a loop to continuously generate data and update the chart
    while True:
        # Generate new data
        new_data = generate_data()

        # Update the chart with the new data
        chart.add_rows(new_data)

        # Sleep for the specified interval
        time.sleep(update_interval)


def tre():
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)
    #update_interval = st.slider("Update interval (seconds)", 1, 10, 1)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.5)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


st.title('## live chart !!!')

log = 75203008

def fur():
    mt5.initialize()
    login = log


    #balance = account_info.balance
    ee = []

    def eq(log):
            login = log
            account_info = mt5.account_info()
            login_number = account_info.login
            equity = account_info.equity
            e = int(equity)
            ee.append(e)
            return e
    eq(log)

    #if len(ee)>20:
    #    ee.pop[0]

    X =[] #deque()
    X.append(1)
    if len(X) > 30 :
        X.pop[0]
    Y = [] #deque(maxlen = 20)
    #Y.append(s)

    app = dash.Dash(__name__)

    app.layout = html.Div(
        [
            dcc.Graph(id = 'live-graph', animate = True),
            dcc.Interval(
                id = 'graph-update',
                interval = 1000,
                n_intervals = 10
            ),
        ]
    )

    @app.callback(
        Output('live-graph', 'figure'),
        [ Input('graph-update', 'n_intervals') ]
    )

    def update_graph_scatter(n):
            account_info = mt5.account_info()
            equity = account_info.equity
            ty = int(equity)    
            X.append(X[-1]+1)
            Y.append(eq())
            #X=list(X)
            #X.pop[0]
            data = plotly.graph_objs.Scatter(
                    x=list(X),
                    y=list(Y),
                    name='Scatter',
                    mode= 'lines+markers'
            )
            
            if len(X) > 50 :
                line = max(X) - 50
            else:
                line = min(X)
            return {'data': [data],
                    'layout' : go.Layout(xaxis=dict(range=[line ,max(X)+5]),yaxis = dict(range = [min(Y)-50,max(Y)+50]),)}

    if __name__ == '__main__':
        app.run_server()



def five():
    try:
        import pandas as pd
        import streamlit as st
        import plotly.graph_objects as go
        import time
        def get_equity():
            import MetaTrader5 as mt5
            mt5.initialize()
            login = 51203790
            account_info = mt5.account_info()
            time.sleep(0.5)
            equity = account_info.equity
            equity = int(equity)
            n = pd.Series(equity)
            #jj = pd.DataFrame(n)
            return n
        
        def bal():
            import MetaTrader5 as mt5
            mt5.initialize()
            login = 51203790
            account_info = mt5.account_info()
            time.sleep(0.5)
            balance = account_info.balance
            balance = int(balance)
            k = pd.Series(balance)
            #j = pd.DataFrame(k)
            return k
        
        def jam():
            balance = bal()
            equity = get_equity()
            u = pd.concat([balance, equity], axis=1, keys=['Balance', 'Equity'])
            return u

        
        x = [time.time()]
        chart = st.line_chart( jam(),x=time.time() , width=0, height=0 )
        #i = 50
        def update_graph():
            
            
            
            #fig = go.Figure(data=[go.Scatter(x=x, y=equity, mode='lines+markers')])

            chart.add_rows(jam())
            #chart(fig)
            #progress_bar.progress(i)
            
            

        while True:
            time.sleep(1)
            #i = i+1
            update_graph()
    except Exception as khata :
        if isinstance ( khata,AttributeError) and khata.args[0] == "'NoneType' object has no attribute 'balance'" or  khata.args[0] == "'NoneType' object has no attribute 'equity'"  :
            mt5.initialize()
            login = 51203790
            account_info = mt5.account_info()
            if not mt5.initialize():
                print("متاتریدر از دسترس خازج شده لطفا برسی کنید=",mt5.last_error())
                quit()
        else:
            pass

        print("خطا: ", type(khata).__name__)

    finally:
        print('اتصال شبکه ')




