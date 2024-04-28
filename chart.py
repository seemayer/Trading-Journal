from functions import *
import pandas as pd
from lightweight_charts.widgets import StreamlitChart
import datetime
import streamlit as st

# https://lightweight-charts-python.readthedocs.io/en/latest/index.html

def create_chart(ticker,stock_data,buy_date,buyprice,stop,target,sell_date,sellprice):


    chart = StreamlitChart(width=1200, height=500)
    chart.watermark(ticker, color='rgba(180, 180, 240, 0.7)')
    # chart.layout(background_color='white')
    # chart.grid(False)
    stock_data.to_csv('./stockdata.csv', index=False)

    chart.set(stock_data)
    
    linenddate = adddaystodatestring(buy_date,20)
    
    #buy line
    line = chart.create_line('buyprice',price_line=False,price_label=False,color='blue',width=2)
    line.set(pd.DataFrame([{'time': buy_date, 'buyprice': buyprice}, {'time': linenddate, 'buyprice': buyprice}]))
    #stop line
    line = chart.create_line('stop',price_line=False,price_label=False,color='red',width=2)
    line.set(pd.DataFrame([{'time': buy_date, 'stop': stop}, {'time': linenddate, 'stop': stop}]))
    # target line
    line = chart.create_line('target',price_line=False,price_label=False,color='green',width=2)
    line.set(pd.DataFrame([{'time': buy_date, 'target': target}, {'time': linenddate, 'target': target}]))
    
    
    chart_start = adddaystodatestring(buy_date,-50)
    chart_end = datetime.date.today().strftime("%Y-%m-%d")

    
    

    chart.marker(buy_date,text='Buy',position='below',shape='arrow_up',color='green')
    if sell_date: 
        line = chart.create_line('sell',price_line=False,price_label=False,color='red',width=2)
        line.set(pd.DataFrame([{'time': sell_date, 'sell': sellprice}, {'time': adddaystodatestring(sell_date,20), 'sell': sellprice}]))
        chart.marker(sell_date,text='Sell',position='above',shape='arrow_down',color='red')
        chart_end = adddaystodatestring(sell_date,20)


    chart.set_visible_range(chart_start,chart_end)
    chart.load()

    # st.write("Hello")
