import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data
import datetime
import yfinance as yf
from flask import Flask, jsonify



def datahandler(ticker,start_date,end_date):
    print(f'Getting stock data for {ticker}')

    df = yf.download(ticker, start=start_date, end= end_date) # download data from yahoo
    
    # Convert df to correct format for Lightweight Charts
    df['time']=df.index.format() #Convert timestamp to string
    df.columns = df.columns.str.lower() #rename columns to lower case
    df.rename(columns={'Volume': 'Values'}, inplace=True)
    df = df.fillna(0) # Replace NaN with zeros

    # print(f'Data frame data for {ticker}:\n {df.head(5)}')
    dict = df.to_dict(orient='records') #convert to dictionary
        
    return dict

ticker = st.text_input("Enter Ticker","GOOG")

chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

st.subheader("Data Toggling for an Area Chart")

data_select = st.sidebar.radio('Select data source:', ('Area 01', 'Area 02'))

today = datetime.datetime.now()
next_year = today.year
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

selected_date = st.date_input(
    "Select time period",
    (jan_1, datetime.date(next_year, 1, 7)),
    min_value=jan_1,
    max_value=dec_31,
    format="MM.DD.YYYY"
)



if selected_date:
    st.write("You selected:", selected_date)
    
    stock_data=datahandler(ticker,selected_date[0],selected_date[1])

if data_select == 'Area 01':
    renderLightweightCharts( [
        {
            "chart": chartOptions,
            "series": [{
                "type": 'Candlestick',
                "data": stock_data,
                "options": {}
            }],
        }
    ], 'area')
else:
    renderLightweightCharts( [
        {
            "chart": chartOptions,
            "series": [{
                "type": 'Area',
                "data": data.seriesMultipleChartArea02,
                "options": {}
            }],
        }
    ], 'area')
