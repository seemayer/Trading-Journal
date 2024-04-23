from grid import *

import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import datetime
import yfinance as yf
import pandas as pd


import st_aggrid as st_ag
import pandas_ta as ta

st. set_page_config(layout="wide")

def get_stock_data(ticker,start_date,end_date):
    print(f'Getting stock data for {ticker}')

    df = yf.download(ticker,start=start_date,end=end_date)[['Open', 'High', 'Low', 'Close', 'Volume']] # download data from yahoo
    df['Volume'] = df['Volume'].astype(float)
    print(df.dtypes)

    # Convert df to correct format for Lightweight Charts
    df = df.reset_index()
    df.columns = ['time','open','high','low','close','volume']                  # rename columns
    df['time'] = df['time'].dt.strftime('%Y-%m-%d')                             # Date to string
    df.rename(columns={'Volume': 'Values'}, inplace=True)                
    df = df.fillna(0) # Replace NaN with zeros

    # print(f'Data frame data for {ticker}:\n {df.head(5)}')
    dict = df.to_dict(orient='records') #convert to dictionary
        
    return dict

def adddaystodatestring(start_date,days):
    date_1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = date_1 + datetime.timedelta(days)
    end_date_str = end_date.strftime("%Y-%m-%d")  # Convert back to string
    return end_date_str

def convertdatestring(sDate):
    return datetime.datetime.strptime(sDate, '%d/%m/%Y').strftime('%Y-%m-%d')    

st.subheader("Trade Chart")

control_container = st.container(border=True)
chart_container = st.container(border=True)
table_container = st.container(border=True)

with table_container:
    
    df = pd.read_csv("./data.csv")
    data = create_grid(df)

    # Process selected row
    selected_rows = data['selected_rows'].iloc[0]
    # st.dataframe(data['selected_rows'])

    ticker = selected_rows["Ticker"]
    start = convertdatestring(selected_rows["Date"])
    end = adddaystodatestring(convertdatestring(selected_rows["Date"]),100)
    sell_date = selected_rows["Close_Date"]
    if sell_date:
        sell_date=convertdatestring(sell_date)
        end=sell_date
        
    stop = float(selected_rows["Stop"] or 0)
    target = float(selected_rows["Target"] or 0)
    buyprice = float(selected_rows["Entry_Price"] or 0) 
    sellprice = float(selected_rows["Close_Price"] or 0)

    stock_data=get_stock_data(ticker,start,end)
    
    
    data['data'].to_csv("./output.csv", index=False)



with control_container:
    
    selected_date = st.date_input(
        "Select time period",
        (datetime.datetime.strptime(start,"%Y-%m-%d"), datetime.datetime.strptime(end,"%Y-%m-%d")),
        max_value=datetime.datetime.now(),
        format="MM.DD.YYYY"
    )

    if selected_date:
        # st.write("You selected:", selected_date)    
        stock_data=get_stock_data(ticker,selected_date[0] - datetime.timedelta(days=100),selected_date[1] + datetime.timedelta(days=100))

with chart_container:
    
    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        },
        "timeScale" : {
            "borderColor":'#ff0000',
            "visible":True,
        }
    }

    seriesOptions = [
            {
                "type": 'Candlestick',
                "data": stock_data,
                "options": {},
                "markers": [
                {
                    "time": start,
                    "position": 'belowBar',
                    "color": 'rgba(67, 83, 254, 1)',
                    "shape": 'arrowUp',
                    "text": 'BUY',
                    "size": 1
                }
                ]
            },
            { #stop
                "type": 'Line', 
                "data": [
                    { "time": start, "value": stop },
                    { "time": adddaystodatestring(start,10), "value": stop }
                ],
                "options": {
                    "color":"red",
                    "lineWidth":1,
                    "lastValueVisible": False,
                    "priceLineVisible": False
                }                
            },
            { #target
                "type": 'Line',
                "data": [
                    { "time": start, "value": target },
                    { "time": adddaystodatestring(start,10), "value": target }
                ],
                "options": {
                    "color":"green",
                    "lineWidth":1,
                    "lastValueVisible": False,
                    "priceLineVisible": False                    
                }
            },
            { #buyline
                "type": 'Line', 
                "data": [
                    { "time": start, "value": buyprice },
                    { "time": adddaystodatestring(start,10), "value": buyprice }
                ],
                "options": {
                    "color":"blue",
                    "lineWidth":1,
                    "lastValueVisible": False,
                    "priceLineVisible": False
                }                
            }            
            ]

    if sell_date:
        seriesOptions[0]['markers'].append(
                    {
                        "time": sell_date,
                        "position": 'aboveBar',
                        "color": 'rgba(67, 83, 254, 1)',
                        "shape": 'arrowDown',
                        "text": 'SELL',
                        "size": 1
                    })
        seriesOptions.append(
            { #sellline
                "type": 'Line', 
                "data": [
                    { "time": sell_date, "value": sellprice },
                    { "time": adddaystodatestring(sell_date,10), "value": sellprice }
                ],
                "options": {
                    "color":"blue",
                    "lineWidth":1,
                    "lastValueVisible": False,
                    "priceLineVisible": False
                }                
            } 
        )


    renderLightweightCharts([{"chart": chartOptions,"series": seriesOptions}])
