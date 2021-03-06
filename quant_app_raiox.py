import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
#import time
#import matplotlib.pyplot as plt
import plotly.express as px
#import seaborn as sns
#import cufflinks as cf
#import datetime
from datetime import date
import math


def raiox():
    st.header('Raio-X do Mercado')
    st.markdown('***')
    df_lista_bolsas = pd.read_csv('./Indices_Bolsas_Mundo.csv')
    count = 0
    df_lista_bolsas['Ult. Preço'] = ''
    df_lista_bolsas['%'] = ''
    for (pais, indice) in zip(df_lista_bolsas['País'], df_lista_bolsas['index_yf']):
      price = yf.download(indice, period='5d', progress=False)['Adj Close']
      change = (((price.iloc[-1] - price.iloc[-2]) / price.iloc[-2]) * 100).round(2)
      df_lista_bolsas['Ult. Preço'][count] = price.iloc[-1]
      df_lista_bolsas['%'][count] = change
      count += 1

    st.subheader('**Comportamento das Bolsas pelo Mundo**')
    st.markdown(str(date.today().strftime('%d/%m/%Y')))
    fig = px.choropleth(df_lista_bolsas, locations="Sigla", hover_data=['País', 'Indice', '%'])
    fig.update_layout(showlegend=False,
                    margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_traces(colorscale=[(0.00, "red"), (0.50, "red"), (0.50, "green"), (1.00, "green")], zmid=0,
                    z=df_lista_bolsas['%'])
    st.plotly_chart(fig)
    st.markdown('***')

    for i in range(0,16,3):
        col1, col2, col3 = st.columns(3)
        col1.metric(str(df_lista_bolsas.iloc[i][0] + '-' + df_lista_bolsas.iloc[i][1]), value="%.2f" % df_lista_bolsas.iloc[i][4], delta=str(df_lista_bolsas.iloc[i][5]) + '%')
        col2.metric(str(df_lista_bolsas.iloc[i+1][0] + '-' + df_lista_bolsas.iloc[i+1][1]), value="%.2f" % df_lista_bolsas.iloc[i+1][4], delta=str(df_lista_bolsas.iloc[i+1][5]) + '%')
        col3.metric(str(df_lista_bolsas.iloc[i+2][0] + '-' + df_lista_bolsas.iloc[i+2][1]), value="%.2f" % df_lista_bolsas.iloc[i+2][4], delta=str(df_lista_bolsas.iloc[i+2][5]) + '%')

    st.markdown('Dados com delay de 15 min.')
    st.markdown('***Página em desenvolvimento e testes***')
