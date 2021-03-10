import streamlit as st
import pandas as pd
import datetime

import altair as alt
from iexfinance.stocks import get_historical_data

import json
token = json.load(open("iexfinance_token.json")).get("token")

tech_list = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'FB', 'BABA', 'TSLA', 'NVDA', 'PYPL', 'INTC',
             'CRM', 'AMD', 'ATVI', 'MTCH', 'EA', 'TTD', 'ZG', 'YELP']

tday = datetime.date.today()
start = tday - datetime.timedelta(days=30)

@st.cache
def load_data(ticker):
    df = get_historical_data(ticker, start, tday, output_format='pandas', token=token)
    df['date'] = df.index
    return df


st.write("""
# Big Tech Stock Price App

""")

ticker = st.selectbox('Company: ', tech_list)

if ticker:

    source = pd.DataFrame({
        'date': load_data(ticker)['date'],
        f'{ticker} value': load_data(ticker)['fClose']
    })

    c = alt.Chart(source).mark_line().encode(x='date', y=alt.Y(f'{ticker} value', scale=alt.Scale(zero=False)))
    st.altair_chart(c, use_container_width=True)


if st.button('Show more'):
    st.write(load_data(ticker))

