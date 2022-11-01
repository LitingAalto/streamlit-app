import streamlit as st
import numpy as np
import datetime
import pandas as pd                        
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import time
import math
from datetime import date
from io import BytesIO
warnings.filterwarnings("ignore") 
from pytrends.request import TrendReq as UTrendReq
GET_METHOD='get'
import requests

headers = {
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'Referer': 'https://trends.google.com/',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
}



class TrendReq(UTrendReq):
    def _get_data(self, url, method=GET_METHOD, trim_chars=0, **kwargs):
        return super()._get_data(url, method=GET_METHOD, trim_chars=trim_chars, headers=headers, **kwargs)



st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: black;'>Google Trends</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: darkgrey;'>Automates search and save the needed keywords for modelling</h2>", unsafe_allow_html=True)

start = st.date_input(
"start date of comparison",
datetime.date(2020, 10, 1))
end = st.date_input(
    "end date of comparison",
    date.today()- datetime.timedelta(days=date.today().weekday()+2))



st.markdown("<h5 style='text-align: left; color: black;'>\nInput here keywords and their afflixes for Google trends comparison</h1>", unsafe_allow_html=True)

category = st.text_input('Category name for the keywords set for search', value = 'Mobiililaajakaistaliittymät')
st.text(" ")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
kw_dict = {}
with col1:
    word = st.text_input('Key Word1', value = "Elisa mobiililaajakaista")
    afflix = st.text_input('Afflix1', value = "Elisa")
    kw_dict[word]=afflix
with col2:
    word = st.text_input('Key Word2', value = "Saunalahti mobiililaajakaista")
    afflix = st.text_input('Afflix2', value = "Elisa")
    kw_dict[word]=afflix
with col3:
    word = st.text_input('Key Word3', value = "DNA mobiililaajakaista")
    afflix = st.text_input('Afflix3', value = "DNA")
    kw_dict[word]=afflix
with col4:
    word = st.text_input('Key Word4', value = "Telia mobiililaajakaista")
    afflix = st.text_input('Afflix4', value = "Telia")
    kw_dict[word]=afflix
with col5:
    word = st.text_input('Key Word5', value = "Sonera mobiililaajakaista")
    afflix = st.text_input('Afflix5', value = "Telia")
    kw_dict[word]=afflix
with col6:
    word = st.text_input('Key Word6', value = "Moi mobiililaajakaista")
    afflix = st.text_input('Afflix6', value = "Moi")
    kw_dict[word]=afflix
with col7:
    word = st.text_input('Key Word7')
    afflix = st.text_input('Afflix7')
    kw_dict[word]=afflix

with st.expander("Input more Keywords"):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        word = st.text_input('Key Word8')
        afflix = st.text_input('Afflix8')
        kw_dict[word]=afflix
        st.text(" ")
        word = st.text_input('Key Word13')
        afflix = st.text_input('Afflix13')
        kw_dict[word]=afflix
    with col2:
        word = st.text_input('Key Word9')
        afflix = st.text_input('Afflix9')
        kw_dict[word]=afflix
        st.text(" ")
        word = st.text_input('Key Word14')
        afflix = st.text_input('Afflix14')
        kw_dict[word]=afflix
    with col3:
        word = st.text_input('Key Word10')
        afflix = st.text_input('Afflix10')
        kw_dict[word]=afflix
        st.text(" ")
        word = st.text_input('Key Word15')
        afflix = st.text_input('Afflix15')
        kw_dict[word]=afflix
    with col4:
        word = st.text_input('Key Word11')
        afflix = st.text_input('Afflix11')
        kw_dict[word]=afflix
        st.text(" ")
        word = st.text_input('Key Word16')
        afflix = st.text_input('Afflix16')
        kw_dict[word]=afflix
    with col5:
        word = st.text_input('Key Word12')
        afflix = st.text_input('Afflix12')
        kw_dict[word]=afflix
        st.text(" ")
        word = st.text_input('Key Word17')
        afflix = st.text_input('Afflix17')
        kw_dict[word]=afflix

        

kw_dict = {k: v for k, v in kw_dict.items() if v!=''}

def merge2df(df1, df2):
    df=df1.merge(df2, on='date')
    df['trans']=df[df.filter(regex='_x').columns].values/df[df.filter(regex='_y').columns].values
    df['trans']=df['trans'].fillna(df[df.filter(regex='_x').columns].mean()/df[df.filter(regex='_y').columns].mean())
    for col in df.columns[-(df2.shape[1]-1):-1]:
        if col != 'trans':
            df[col] = df['trans']*df[col]
            df[col] = df[col].fillna(0).apply(lambda x: int(round(x,0)))
    df.drop(df.filter(regex='_y').columns,1, inplace=True)
    df.columns = [ x.split('_x')[0] for x in df.columns]
    return df.drop('trans',1)

def sos_calculator(kw_dict, category = category):
    df=pd.DataFrame()
    search = list(kw_dict.keys())
    t=30
    while len(search)>0:
        time.sleep(t)
        print(search)
        if df.shape[0]>0:
            try:
                pytrend = TrendReq(hl='en-US', tz=0)
                key1=(df.set_index('date') == 0).astype(int).sum(axis=0).sort_values(ascending=True).index[0]
                st.text(search[:4]+[key1])
                pytrend.build_payload(search[:4]+[key1], cat=0, timeframe=duration, geo='FI', gprop='')
                df1 = pytrend.interest_over_time().reset_index().drop('isPartial',1)
                df = merge2df(df, df1)
                st.dataframe(df1)
                st.dataframe(df)
                t+=30
            except:
                st.text(f'No data from below keywordlist:\n{search[:4]+[key1]}')
                t+=60
            search = list(set(search)-set(search[:4]))
        else:
            try:
                st.text(search[:5])
                pytrend2 = TrendReq(hl='en-US', tz=0)
                pytrend2.build_payload(search[:5], cat=0, timeframe=duration, geo='FI', gprop='')
                df1 = pytrend2.interest_over_time().reset_index().drop('isPartial',1)
                df = df1.copy()
                t+=30
            except:
                st.text(f'No data from below keywordlist:\n{search[:5]}')
                t+=60
            search = list(set(search)-set(search[:5]))
    if df.shape[0] ==0:
        st.text('google blocked.. returned 0 data...')
    else:
        df=df.set_index('date')
        df0 = df.copy()
        df2 = df0.reset_index()
        df2['date']=df2['date'].dt.to_period('M').astype('str')
        dfm = df2.groupby('date').mean().dropna()

        df.columns=df.columns.map(kw_dict)
        df = df.groupby(lambda x:x, axis=1).sum()
        df2 = df.reset_index()
        df2['date']=df2['date'].dt.to_period('M').astype('str')
        df2 = df2.groupby('date').mean().dropna() # monthly agg
        return df0.reset_index(), dfm.reset_index(), df2.reset_index()


if st.button('Calculate Google trends'):
    df_weekly, df_monthly, df = sos_calculator(kw_dict, category = category )
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df, x="date", y=list(set(kw_dict.values())), title='Share of Search Over Time (Monthly aggregated)')
        
        st.plotly_chart(fig, use_container_width=True)
        ax = sns.lineplot(data=df.set_index('date'))
        plt.xticks(rotation=90)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True)
        plt.savefig("python.png")
        
    with col2:
        df1=pd.DataFrame()
        df1['share']=(df.mean()/(df.mean().sum())).values
        df1['names']=(df.mean()/(df.mean().sum())).index
        fig1 = px.pie(df1, values='share', names='names', title='Share of Search in %',hole=.65)
        #fig1.show()  
        st.plotly_chart(fig1, use_container_width=True)
        

    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df_weekly.to_excel(writer, index=False, sheet_name='weekly_orign')
        df_monthly.to_excel(writer, index=False, sheet_name='monthly_orign')
        workbook = writer.book
        worksheet = workbook.add_worksheet("Plot(Monthly aggregated)")
        worksheet.insert_image('B2', 'python.png', {'x_offset': 15, 'y_offset': 1})
        writer.save()
        processed_data = output.getvalue()
        return processed_data
    df_xlsx = to_excel(df)
    file = st.text_input('Name your file', value='5G google trends')
    st.download_button(label='📥 Download trends data from the selected keywords',
                                    data=df_xlsx ,
                                    file_name= f'{file}.xlsx')
