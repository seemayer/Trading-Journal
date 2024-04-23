from grid import *
from chart import *
from functions import *

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.subheader("Trade Chart")

#set up widget order
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
    create_chart(stock_data,start,buyprice,stop,target,sell_date,sellprice)
    