import streamlit as st
import datetime
import pandas as pd                        
from pytrends.request import TrendReq
import plotly.express as px
import warnings
warnings.filterwarnings("ignore") 
pytrend = TrendReq(hl='en-US', tz=120, timeout=(5,10))

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: black;'>Google Trends</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: darkgrey;'>Automates search and save the needed keywords for modelling</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    start = st.date_input(
    "start date of comparison",
    datetime.date(2020, 7, 6))
    end = st.date_input(
        "end date of comparison",
        datetime.date(2022, 7, 6))
    duration = str(start)+' '+str(end)
with col2:
    group = st.selectbox(
    'How would you like The data to be aggregated?',
    ('Monthly', 'Weekly'))
with col3:
    if group =='Monthly':
        sm = st.selectbox(
        'How would you like to smooth data?',
        ('No', 'Yes, moving average 12m'))
    else:
        sm = st.selectbox(
        'How would you like to smooth data?',
        ('No', 'Yes, moving average 1m'))
    smoothing = False
    if sm != 'No':
        smoothing = True


st.markdown("<h5 style='text-align: left; color: black;'>\nInput here keywords and their afflixes for Google Trends comparison</h1>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
kw_dict = {}
with col1:
    word = st.text_input('Key Word1', value = "Elisa Samsung Galaxy")
    afflix = st.text_input('Afflix1', value = "Elisa Phone")
    kw_dict[word]=afflix
with col2:
    word = st.text_input('Key Word2', value = "Telia Samsung Galaxy")
    afflix = st.text_input('Afflix2', value = "Telia Phone")
    kw_dict[word]=afflix
with col3:
    word = st.text_input('Key Word3')
    afflix = st.text_input('Afflix3')
    kw_dict[word]=afflix
with col4:
    word = st.text_input('Key Word4')
    afflix = st.text_input('Afflix4')
    kw_dict[word]=afflix
with col5:
    word = st.text_input('Key Word5')
    afflix = st.text_input('Afflix5')
    kw_dict[word]=afflix

with st.expander("Input more Keywords"):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        word = st.text_input('Key Word6')
        afflix = st.text_input('Afflix6')
        kw_dict[word]=afflix
    with col2:
        word = st.text_input('Key Word7')
        afflix = st.text_input('Afflix7')
        kw_dict[word]=afflix
    with col3:
        word = st.text_input('Key Word8')
        afflix = st.text_input('Afflix8')
        kw_dict[word]=afflix
    with col4:
        word = st.text_input('Key Word9')
        afflix = st.text_input('Afflix9')
        kw_dict[word]=afflix
    with col5:
        word = st.text_input('Key Word10')
        afflix = st.text_input('Afflix10')
        kw_dict[word]=afflix

kw_dict = {k: v for k, v in kw_dict.items() if v!=''}
search = list(kw_dict.keys())

def sos_calculator(search,duration,group, smoothing):
    if len(search)>5:
        pytrend.build_payload(search[:5], cat=0, timeframe=duration, geo='FI', gprop='')
        df1 = pytrend.interest_over_time().reset_index().drop('isPartial',1)
        pytrend.build_payload(search[4:], cat=0, timeframe=duration, geo='FI', gprop='')
        df2 = pytrend.interest_over_time().reset_index().drop('isPartial',1)
        df=df1.merge(df2, on='date')
        df['trans']=df[df.filter(regex='_x').columns].values/df[df.filter(regex='_y').columns].values
        df['trans']=df['trans'].fillna(df['trans'].mean())
        for col in df.columns[6:]:
            if col != 'trans':
                df[col] = df['trans']*df[col]
                df[col] = df[col].apply(lambda x: int(round(x,0)))
        df.drop(df.filter(regex='_y').columns,1, inplace=True)
        df.columns = [ x.split('_x')[0] for x in df.columns]

    else:
        pytrend.build_payload(search, cat=0, timeframe=duration, geo='FI', gprop='')

        df = pytrend.interest_over_time()
        df = df.reset_index()
  
    if group == 'Weekly':
        if smoothing:
            df1 = df.rolling(4).mean()
            df1['date']=df['date']
            df=df1.dropna()
    else:
        df['date']=df['date'].dt.to_period('M').astype('str')
        df = df.groupby('date')[search].mean().reset_index().dropna()
        if smoothing:
            df1 = df.rolling(12).mean().dropna()
            df1['date']=df['date']
            df=df1.dropna()
    df=df.set_index('date')
    df.columns=df.columns.map(kw_dict)
    df = df.groupby(lambda x:x, axis=1).sum().reset_index()
    return df
if st.button('Show calculated trends'):
    
    df = sos_calculator(search,duration,group, smoothing)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df, x="date", y=list(kw_dict.values()), title='Share of Search Over Time')
        #fig.show()
        st.plotly_chart(fig, use_container_width=True)
    #if st.button('Save keywords for reporting and modeling'):
        with open('report.txt','a') as f:
            f.write(str(kw_dict)+'\n')
    with col2:
        df1=pd.DataFrame()
        df1['share']=(df.mean()/(df.mean().sum())).values
        df1['names']=(df.mean()/(df.mean().sum())).index
        fig1 = px.pie(df1, values='share', names='names', title='Share of Search in %',hole=.65)
        #fig1.show()  
        st.plotly_chart(fig1, use_container_width=True)
        
if st.button('Add keywords for analysis'):
    with open('report1.txt','a') as f:
        f.write(str(kw_dict)+'\n')
        print(f)
# st.download_button('Download CSV', text_contents, 'text/csv')
# st.download_button('Download keywords in text file', text_contents)  # Defaults to 'text/plain'

with open('report1.txt') as f:
    print(f)
   st.download_button('Download keywords in text file', f)  # Defaults to 'text/plain'

with st.expander('Add Dates to compare change of Google Trends'):
    start1 = st.date_input(
    "start date of the added comparison",
    datetime.date(2020, 7, 6))
    end1 = st.date_input(
        "end date of the added comparison",
        datetime.date(2022, 7, 6))
    duration1 = str(start1)+' '+str(end1)
    df = sos_calculator(search,duration,group, smoothing)
    dfn = sos_calculator(search,duration1,group, smoothing)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df, x="date", y=list(kw_dict.values()), title='Share of Search Over Time')
        
        df1=pd.DataFrame()
        df1['share']=(df.mean()/(df.mean().sum())).values
        df1['names']=(df.mean()/(df.mean().sum())).index
        fig1 = px.pie(df1, values='share', names='names', title='Share of Search in %',hole=.65)
        st.plotly_chart(fig, use_container_width=True) 
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig3 = px.line(dfn, x="date", y=list(kw_dict.values()), title='Share of Search Over Time')
        df1=pd.DataFrame()
        df1['share']=(dfn.mean()/(dfn.mean().sum())).values
        df1['names']=(dfn.mean()/(dfn.mean().sum())).index
        fig4 = px.pie(df1, values='share', names='names', title='Share of Search in %',hole=.65)
        st.plotly_chart(fig3, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)
