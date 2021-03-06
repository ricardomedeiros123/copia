import pandas as pd
import yfinance as yf
import investpy as inv
import matplotlib as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
import fundamentus
import requests
import os
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import cufflinks as cf
#import datetime
#from datetime import date
import math
import quantstats as qs
import monthly_returns_heatmap as mrh
import statsmodels.api
import statsmodels as sm


def precos(ticker, periodo, pct):
    if pct == True:
        df = yf.download(ticker, period = periodo, progress=False)['Adj Close'].pct_change()
    else:
        df = yf.download(ticker, period=periodo, progress=False)['Adj Close']
    return df


prices = precos('PETR4.SA', periodo='1y', pct=False)

tickers = ['BOVA11.SA']
preco = precos(tickers, '1y', False)
retornos = precos(tickers, '1y', True)

retornos.std()




retornos.plot()
######################

ticker = yf.Ticker('PETR4.SA')
ticker.info

info = inv.get_stock_company_profile('petr4', country='brazil')

indice = inv.get_index_information('Bovespa', country='brazil')

ts = TimeSeries(key=ALPHAVANTAGE_API_KEY, output_format='pandas')
ALPHAVANTAGE_API_KEY ='H71270CJ23B0N9U3'
info = ts.get_symbol_search('petr4')


fd = FundamentalData(key=ALPHAVANTAGE_API_KEY, output_format='pandas')

info = fd.get_company_overview('IBM')

info = fundamentus.get_papel('ALZR11')

setor = fundamentus.get_papel('WEGE3')['Setor'][0]
subsetor = fundamentus.get_papel('WEGE3')['Subsetor'][0]

df = fundamentus.get_resultado()

########### Teste de Rentabilidadde da Carteira

tickers = ['PETR4.SA','VALE3.SA','CSNA3.SA']

carteira = yf.download(tickers, period='1y')['Adj Close']
carteira.dropna(inplace=True)

portifolio = pd.DataFrame({'Ação': ['PETR4.SA','VALE3.SA', 'CSNA3.SA'],'Qtde': [200,300,400],'Setor':['Combustíveis','Financeiro','Utilidades'], 'SubSetor':['Petroleo', 'Bolsa', 'Eletrico']})

valor_carteira = pd.DataFrame()
var_carteira = pd.DataFrame()
for ativo in carteira.columns:
    var_carteira['Var '+ ativo] = ((carteira[ativo]/carteira[ativo].iloc[0])-1)*100
    valor_carteira['Total '+ativo] = carteira[ativo] * portifolio[portifolio['Ação'] == ativo]['Qtde'].iloc[0]

valor_carteira['Total Carteira'] = valor_carteira.sum(axis=1)
var_carteira['Var Carteira'] = ((valor_carteira['Total Carteira']/valor_carteira['Total Carteira'].iloc[0])-1) * 100

ibov = yf.download('^BVSP', period='1y')['Adj Close']
ibov.dropna(inplace=True)
ibov_var_pct = ((ibov / ibov.iloc[0]) - 1) * 100

var_carteira['Var IBOV'] = ibov_var_pct

var_carteira.plot()

qs.extend_pandas()
stock = qs.utils.download_returns('PETR4.SA')
qs.plots.monthly_heatmap(stock)

retornos = yf.download('PETR4.SA')['Adj Close'].pct_change()
mrh.plot(retornos)

ibov = yf.download('^BVSP')['Adj Close']

decomposicao = sm.tsa.seasonal.seasonal_decompose(ibov, model='additive', freq=251)

novo = sm.tsa.seasonal.seasonal_decompose(ibov, model='additive', period=251)



################ BackTesting ################

import bt
data = bt.get('spy,agg', start='2010-01-01')
# create the strategy
s = bt.Strategy('s1', [bt.algos.RunMonthly(),
                       bt.algos.SelectAll(),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])
# create a backtest and run it
test = bt.Backtest(s, data)
res = bt.run(test)

# first let's see an equity curve
res.plot()
res.display()

import ffn
data = ffn.get('vale3.sa', start='2000-01-01', end='2020-12-31')
perf = data.calc_stats()

start_dt = 'Set'
end_dt = 'Dez'

mes_inicio = {'Jan': '-01-01','Fev':'-02-01','Mar':'-03-01','Abr':'-04-01','Mai':'-05-01','Jun':'-06-01','Jul':'-07-01', 'Ago': '-08-01','Set': '-09-01','Out':'-10-01','Nov':'-11-01','Dez':'-12-01'}
mes_fim = {'Jan': '-01-31','Fev':'-02-28','Mar':'-03-31','Abr':'-04-30','Mai':'-05-31','Jun':'-06-30','Jul':'-07-31', 'Ago': '-08-31','Set': '-09-30','Out':'-10-31','Nov':'-11-30','Dez':'-12-31'}

ret = pd.DataFrame()

for ano in range(2000,2021,1):
    print(ano)
    inicio = str(ano) + str(mes_inicio[start_dt])
    fim = str(ano) + str(mes_fim[end_dt])
    perf.set_date_range(start=inicio, end=fim)
    stat = perf.stats
    ret = ret.append({'%': stat.iloc[3].values, 'Ano': ano}, ignore_index=True)

gain = (sum(ret['%'] > 0))
loss = (sum(ret['%'] < 0))

print('Qtde Trades: ', len(ret))
print('Gain: ',gain)
print('Loss: ',loss)




########### Puxar Sstatus Bolsas pelo Mundo ###########

url = 'http://www.grafbolsa.com/index.html'
tabela = pd.read_html(url)[1][3:]  # Pega a 2º tabela, da 3º linha para baixo
tabela = tabela.sort_values(9)  # Classifica em ordem alfabetica pela coluna do código
tabela[9]

url = 'https://br.investing.com/indices/major-indices'
tabela = pd.read_html(url)



###############SpanSlelector MATPLOTLIB###########


import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

def onselect_function(min_value, max_value):
	print(min_value, max_value)
	return min_value, max_value

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [10, 50, 100])

span = SpanSelector(
		ax,
		onselect=onselect_function,
		direction='horizontal',
		minspan=0.1,
		useblit=True,
		span_stays=True,
		button=1,
		rectprops={'facecolor': 'yellow', 'alpha': 0.3}
	)

plt.show()



########################### Altair Graphs ############################

import altair as alt
import pandas as pd
import numpy as np

x = np.random.normal(size=100)
y = np.random.normal(size=100)

m = np.random.normal(15, 1, size=100)

source = pd.DataFrame({"x": x, "y":y, "m":m})

# interval selection in the scatter plot
pts = alt.selection(type="interval", encodings=["x"])

# left panel: scatter plot
points = alt.Chart().mark_point(filled=True, color="black").encode(
    x='x',
    y='y'
).transform_filter(
    pts
).properties(
    width=300,
    height=300
)

# right panel: histogram
mag = alt.Chart().mark_bar().encode(
    x='mbin:N',
    y="count()",
    color=alt.condition(pts, alt.value("black"), alt.value("lightgray"))
).properties(
    width=300,
    height=300
).add_selection(pts)

# build the chart:
alt.hconcat(
    points,
    mag,
    data=source
).transform_bin(
    "mbin",
    field="m",
    bin=alt.Bin(maxbins=20)
)

########################### Plotly Buttons ############################

import yfinance as yf

import pandas as pd
import plotly.graph_objects as go

# Request stocks data for Microsoft (MSFT)
MSFT = yf.Ticker("MSFT")
df_MSFT = MSFT.history(period="max")

# Request stocks data for Apple (AAPL)
AAPL = yf.Ticker("AAPL")
df_AAPL = AAPL.history(period="max")

# Request stocks data for Amazon (AMZN)
AMZN = yf.Ticker("AMZN")
df_AMZN = AMZN.history(period="max")

# Request stocks data for Google (GOOGL)
GOOGL = yf.Ticker("GOOGL")
df_GOOGL = GOOGL.history(period="max")

df_stocks = pd.DataFrame({
    'MSFT': df_MSFT['High'],
    'AAPL': df_AAPL['High'],
    'AMZN': df_AMZN['High'],
    'GOOGL': df_GOOGL['High'],
})

# How to change plot data using dropdowns
#
# This example shows how to manually add traces
# to the plot and configure the dropdown to only
# show the specific traces you allow.

fig = go.Figure()

for column in df_stocks.columns.to_list():
    fig.add_trace(
        go.Scatter(
            x = df_stocks.index,
            y = df_stocks[column],
            name = column
        )
    )
    
fig.update_layout(
    updatemenus=[go.layout.Updatemenu(
        active=0,
        buttons=list(
            [dict(label = 'All',
                  method = 'update',
                  args = [{'visible': [True, True, True, True]},
                          {'title': 'All',
                           'showlegend':True}]),
             dict(label = 'MSFT',
                  method = 'update',
                  args = [{'visible': [True, False, False, False]}, # the index of True aligns with the indices of plot traces
                          {'title': 'MSFT',
                           'showlegend':True}]),
             dict(label = 'AAPL',
                  method = 'update',
                  args = [{'visible': [False, True, False, False]},
                          {'title': 'AAPL',
                           'showlegend':True}]),
             dict(label = 'AMZN',
                  method = 'update',
                  args = [{'visible': [False, False, True, False]},
                          {'title': 'AMZN',
                           'showlegend':True}]),
             dict(label = 'GOOGL',
                  method = 'update',
                  args = [{'visible': [False, False, False, True]},
                          {'title': 'GOOGL',
                           'showlegend':True}]),
            ])
        )
    ])

fig.show()




import fundamentus
from st_aggrid import AgGrid
import pandas as pd

df = fundamentus.get_resultado()
df.reset_index(inplace=True)
AgGrid(df)
