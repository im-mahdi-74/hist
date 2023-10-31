import streamlit as st
import pandas as pd
import numpy as np




from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans as KMeans
from sklearn.linear_model import SGDRegressor as sgd
from sklearn.model_selection import RandomizedSearchCV , GridSearchCV

import matplotlib.pyplot as plt
import missingno as msno
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import seaborn as sns


st.title('ML pages!')


def perpross_num(df):
    # تفکیک ستون ها به زمان 
    def time_sort(df):
        df['open_day']   = df['Time'].apply(lambda x: x.day)
        df['open_hour']  = df['Time'].apply(lambda x: x.hour)
        df['open_min']   = df['Time'].apply(lambda x: x.minute)
        df['close_day']  = df['Time_1'].apply(lambda x: x.day)
        df['close_hour'] = df['Time_1'].apply(lambda x: x.hour)
        df['close_min']   = df['Time_1'].apply(lambda x: x.minute)

        columns_to_remove = ['Time', 'Time_1']
        df = df.drop(columns=columns_to_remove , axis = 1)
        return df

    #پیش پردازش 
    def perpros(df):
        df = pd.get_dummies(df)
        df = df.astype(float)
        df.fillna(0, inplace=True)

        return df

    df = time_sort(df)
    df = perpros(df)
    df.fillna(0, inplace=True)
    df_cleaned = df[~df.applymap(lambda x: np.isinf(x) or pd.isna(x)).any(axis=1)]
    df_cleaned = df_cleaned.reindex()
    return df_cleaned

def outlier(df):
    # محاسبه Z-score برای هر مقدار
    column_name = 'deltaM'
    z_scores = np.abs((df[column_name] - df[column_name].mean()) / df[column_name].std())

    # تعیین آستانه (threshold) برای تشخیص اوتلایرها
    threshold = 1  # می‌توانید آستانه را تغییر دهید

    # حذف ردیف‌هایی که Z-score آنها بیشتر از آستانه است
    df_no_outliers = df[z_scores <= threshold]
    st.write(f'shiape befor remove outlier {df.shape} , after {df_no_outliers.shape}')

    def outlier_abspipeg(df):
        # محاسبه Z-score برای هر مقدار
        column_name = 'ABSpipeg'
        z_scores = np.abs((df[column_name] - df[column_name].mean()) / df[column_name].std())

        # تعیین آستانه (threshold) برای تشخیص اوتلایرها
        threshold = 2  # می‌توانید آستانه را تغییر دهید

        # حذف ردیف‌هایی که Z-score آنها بیشتر از آستانه است
        df_no_outliers = df[z_scores <= threshold]
        st.write(f'shiape befor remove outlier {df.shape} , after {df_no_outliers.shape}')
        return df_no_outliers
    


    def outlier_abspipegg(df):
        # محاسبه Z-score برای هر مقدار
        column_name = 'V/B'
        z_scores = np.abs((df[column_name] - df[column_name].mean()) / df[column_name].std())

        # تعیین آستانه (threshold) برای تشخیص اوتلایرها
        threshold = 0.7  # می‌توانید آستانه را تغییر دهید

        # حذف ردیف‌هایی که Z-score آنها بیشتر از آستانه است
        df_no_outliers = df[z_scores <= threshold]
        st.write(f'shiape befor remove outlier {df.shape} , after {df_no_outliers.shape}')
        return df_no_outliers


    df_no_outlier = outlier_abspipeg(df_no_outliers)
    df_no_vb = outlier_abspipegg(df_no_outlier)

    return df_no_vb



def perpross_scaler(X):

    # استخراج نام ستون‌ها
    columns = X.columns
    X = X.values
    
    # ایجاد آبجکت StandardScaler
    scaler = StandardScaler()  

    # برازش مدل به داده
    X_scaled = scaler.fit_transform(X)

    
    X_scaled = pd.DataFrame(X_scaled, columns=columns)
    X_scaled
    #st.write(X_scaled.mean(),X_scaled.var())
   
    
    return X_scaled

def plot_histogram(df, column):
    """
    Plots a histogram of the given column from the DataFrame.

    Args:
        df: The DataFrame to plot from.
        column: The column to plot.

    Returns:
        The Streamlit component for the histogram.
    """

    fig = px.histogram(df, x=column)
    st.plotly_chart(fig)

def scatter(df , x , y):

    fig_2d = px.scatter(df, x=df[x], y=df[y])
    fig_2d.update_layout(width=700, height=1000)
    fig_2d.update_traces(marker=dict(size=2))
    st.plotly_chart(fig_2d)

def box_hist(df, col_name):
    # Create the box plot with a notch
    fig = px.box(df, x=col_name, points='all')
    # Display the box plot in Streamlit
    st.plotly_chart(fig)


def k_mean(df):
    df = df[['PP', 'deltaM']]
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
        #k-means++ is an algorithm for choosing the initial values (or "seeds") for the k-means clustering algorithm.
        kmeans.fit(df)
        wcss.append(kmeans.inertia_) 
    def wcss(wcss):
        plt.plot(range(1, 11), wcss)
        plt.title('The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        st.pyplot(plt)     
    kmeans = KMeans(n_clusters = 4, init = 'k-means++', random_state = 42)
    y_kmeans = kmeans.fit_predict(df)
    st.write(kmeans.cluster_centers_)

    # ایجاد یک DataFrame نمونه برای داده‌ها
    data = {'PP': [2.1395, 0.1691, -0.9603, -0.6198],
            'Cluster Centers (k-means)': [0.18, -0.1199, -0.1711, 8.8339]}
    data = pd.DataFrame(data)

    # ایجاد نمودار Scatter Plot با دو مجموعه نقاط
    fig = px.scatter(df , x='PP', y='deltaM', width= 900 , height= 700 )



    # نمایش نمودار در Streamlit
    st.plotly_chart(fig)

def heatmap(df):
    st.write(df.corr())
    correlation_matrix = df.corr()

    # ایجاد Heatmap با Plotly Express
    fig = px.imshow(correlation_matrix, width=1000, height=1200)
    st.plotly_chart(fig)

@st.cache_data(ttl='1h' , max_entries=1 )
def regression_for_pipeg(df):
    df = df.drop('deltaM' , axis = 1)
    df = df[[col for col in df if col != 'ABSpipeg'] + ['ABSpipeg']]
    df
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    train_df = np.array(train_df)
    test_df = np.array(test_df)

    x_train = np.delete(train_df, -1 , axis=1)
    y_train = train_df[:, [-1]]
    x_train.shape , y_train.shape
    x_train
    y_train
    
    model = sgd(random_state=1)
    lrs = np.logspace(-3, 0 , 50)
    alphas = np.logspace(-6, 0 , 50)
    param_distr = {'eta0' : lrs , 'alpha':alphas}

    random_serach = RandomizedSearchCV(model , param_distr , n_iter=1500 , random_state= 2)
    random_serach.fit(x_train , y_train.ravel())

    random_serach.best_params_ , random_serach.best_score_

    lr, alpha = random_serach.best_params_.values()

    d1, d2 = 0.1, 0.1
    lrs = np.r_[np.linspace((1-d1)*lr, (1+d1)*lr, 50), lr]
    alphas = np.r_[np.linspace((1+d2)*alpha, (1+d2)*alpha, 50), alpha]

    param_grid = {'eta0': lrs, 'alpha': alphas}
    grid_search = GridSearchCV(model, param_grid)
    grid_search.fit(x_train, y_train.ravel())

    # Best parameters
    grid_search.best_params_, grid_search.best_score_

    model = grid_search.best_estimator_
    model.coef_, model.intercept_






if 'ml' in st.session_state:
    df = st.session_state.ml
    
    df = perpross_num(df)
    df = outlier(df)
    if 'Balance_now' in df.columns:
        df = df.drop('Balance_now', axis=1)

    print(df.columns)
    st.title('Standard Scale')
    df.to_csv('pycarettest_main_tow.csv', index= False )
    df_scale = perpross_scaler(df)
    df_scale.to_csv('pycarettest_main.csv', index= False )
    df_scale = df_scale.drop(['close_day', 'close_hour','close_min','Profit', 'Price_1', 'Commission', 'Swap' , 'ABSPP','PP', 'deltaH',  '-pipeg/deltaH', '-pipeg/deltaM', '-pipeg/Balance', '-pipeg/VB', '-PP' , '-PP/deltaH','-PP/deltaM', 'ABSPP%VB', 'deltaH/VB', 'deltaM/VB', 'ABSPP/deltaH','ABSPP/deltaM', '+pipeg', '+pipeg/deltaH', '+pipeg/deltaM','+pipeg/Balance', '+pipeg/VB', '+P', '+PP', '+PPVB', '+PP/deltaH','+PP/deltaM', '-pipeg', '-PPVB', '-P' ] , axis=1 )
    print(df_scale.columns)
    df_scale
    df_scale.to_csv('pycarettest_two.csv', index= False )
    st.write('انتخاب ستون برای هیستوگرام')

    column = st.selectbox("Select column to plot", df_scale.columns , key='histogram_col')
    plot_histogram(df_scale,column)
    st.write('انتخاب ستون برای باکس پلات')
    col_name = st.selectbox("Select a column", df_scale.columns , key= 'box_hist')
    box_hist(df, col_name)
    heatmap(df_scale)

    st.write('انتخاب ستون برای scatter ')
    x_col = st.selectbox('Select X column', df_scale.columns, key= 'x_col')
    y_col = st.selectbox('Select Y column', df_scale.columns, key = 'y_col')

    scatter(df_scale , x_col , y_col)
    if st.button('انجام رگرسیون خطی روی '):
        regression_for_pipeg(df_scale)




    #k_mean(df_scale)

else:
    st.write('file not fund')










