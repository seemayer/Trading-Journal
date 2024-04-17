import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import datetime
import yfinance as yf
import pandas as pd

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

def convertdata(list_of_dictionaries):
    df = pd.DataFrame(list_of_dictionaries)
    df = df[['time','close']]
    df = df.rename(columns={'close': 'value'})
    dict = df.to_dict(orient='records') #convert to dictionary
    return dict


st.subheader("Data Toggling for an Area Chart and Candlestick")

my_query_params = st.query_params.to_dict()
ticker = my_query_params["ticker"]
start = datetime.datetime.strptime(my_query_params["start"],"%Y-%m-%d")
end = datetime.datetime.strptime(my_query_params["end"],"%Y-%m-%d")

st.write("My Query Params:",ticker,start,end)

stock_data=datahandler(my_query_params["ticker"],my_query_params["start"],my_query_params["end"])

selected_date = st.date_input(
    "Select time period",
    (start, end),
    max_value=datetime.datetime.now(),
    format="MM.DD.YYYY"
)

if selected_date:
    st.write("You selected:", selected_date)    
    stock_data=datahandler(ticker,selected_date[0],selected_date[1])

chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

data_select = st.sidebar.radio('Select chart type source:', ('Candlestick', 'Area'))

if data_select == 'Candlestick':
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
                "data": convertdata(stock_data),
                "options": {}
            }],
        }
    ], 'area')   
