import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import datetime
import yfinance as yf
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode

st. set_page_config(layout="wide")

def get_stock_data(ticker,start_date,end_date):
    print(f'Getting stock data for {ticker}')

    df = yf.download(ticker, start=start_date, end=end_date) # download data from yahoo
    print(df.dtypes)

    # Convert df to correct format for Lightweight Charts
    df['time']=df.index.format() #Convert timestamp to string
    print(df)
    df.columns = df.columns.str.lower() #rename columns to lower case
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

df = pd.read_csv("./data.csv")

st.subheader("Data Toggling for an Area Chart and Candlestick")

control_container = st.container(border=True)
chart_container = st.container(border=True)
table_container = st.container(border=True)

with table_container:
    # Configure the grid
    #gb = GridOptionsBuilder.from_dataframe(df[['Date', 'Ticker']])
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode='single', use_checkbox=True)
    gb.configure_default_column(editable=True)
    gb.configure_column("Date", editable=False)
    gb.configure_side_bar()
    gridOptions = gb.build()

    # Display the grid
    data = AgGrid(df, gridOptions=gridOptions,
                editable=True, 
                enable_enterprise_modules=True, 
                allow_unsafe_jscode=True, 
                update_mode=GridUpdateMode.VALUE_CHANGED | GridUpdateMode.SELECTION_CHANGED, 
                columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)

    # Process selected row
    selected_rows = data['selected_rows']
    st.dataframe(data['selected_rows'])



    ticker = selected_rows.iloc[0]["Ticker"]
    start = convertdatestring(selected_rows.iloc[0]["Date"])
    end = adddaystodatestring(convertdatestring(selected_rows.iloc[0]["Date"]),100)
    stop = selected_rows.iloc[0]["Stop"]
    target = selected_rows.iloc[0]["Target"]

    stock_data=get_stock_data(ticker,start,end)

with control_container:
    selected_date = st.date_input(
        "Select time period",
        (datetime.datetime.strptime(start,"%Y-%m-%d"), datetime.datetime.strptime(end,"%Y-%m-%d")),
        max_value=datetime.datetime.now(),
        format="MM.DD.YYYY"
    )

    if selected_date:
        st.write("You selected:", selected_date)    
        stock_data=get_stock_data(ticker,selected_date[0] - datetime.timedelta(days=10),selected_date[1] + datetime.timedelta(days=10))

with chart_container:
    
    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }    

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
                    { "time": adddaystodatestring(start,10), "value": stop }
                ],
                "options": {"color":"red"}
            },
            { #target
                "type": 'Line',
                "data": [
                    { "time": start, "value": target },
                    { "time": adddaystodatestring(start,10), "value": target }
                ],
                "options": {"color":"green"}
            }
            ],
        }
    ], 'area')
