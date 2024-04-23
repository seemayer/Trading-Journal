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

def adddaystodatestring(start_date):
    date_1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = date_1 + datetime.timedelta(days=10)
    end_date_str = end_date.strftime("%Y-%m-%d")  # Convert back to string
    return end_date_str


st.subheader("Data Toggling for an Area Chart and Candlestick")

my_query_params = st.query_params.to_dict()
ticker = my_query_params["ticker"]
start = my_query_params["start"]
end = my_query_params["end"]
stop = my_query_params["stop"]
target = my_query_params["target"]

st.write("My Query Params:",ticker,start,end)

stock_data=datahandler(ticker,start,end)

selected_date = st.date_input(
    "Select time period",
    (datetime.datetime.strptime(start,"%Y-%m-%d"), datetime.datetime.strptime(end,"%Y-%m-%d")),
    max_value=datetime.datetime.now(),
    format="MM.DD.YYYY"
)

if selected_date:
    st.write("You selected:", selected_date)    
    stock_data=datahandler(ticker,selected_date[0] - datetime.timedelta(days=10),selected_date[1] + datetime.timedelta(days=10))

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
            "series": [
            {
                "type": 'Candlestick',
                "data": stock_data,
                "options": {},
                "markers": [
                {
                    "time": end,
                    "position": 'aboveBar',
                    "color": 'rgba(67, 83, 254, 1)',
                    "shape": 'arrowDown',
                    "text": 'SELL',
                    "size": 3
                },
                {
                    "time": start,
                    "position": 'belowBar',
                    "color": 'rgba(67, 83, 254, 1)',
                    "shape": 'arrowUp',
                    "text": 'BUY',
                    "size": 3
                }
                ]
            },
            { #stop
                "type": 'Line',
                "data": [
                    { "time": start, "value": stop },
                    { "time": adddaystodatestring(start), "value": stop }
                ],
                "options": {"color":"red"}
            },
            { #target
                "type": 'Line',
                "data": [
                    { "time": start, "value": target },
                    { "time": adddaystodatestring(start), "value": target }
                ],
                "options": {"color":"green"}
            }
            ],
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
