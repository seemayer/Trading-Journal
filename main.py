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
    
    # Get values from table
    ticker = selected_rows["Ticker"]
    buy_date = convertdatestring(selected_rows["Date"])
    sell_date = convertdatestring(selected_rows["Close_Date"])
    end = sell_date or adddaystodatestring(buy_date,100)
        
    stop = float(selected_rows["Stop"] or 0)
    target = float(selected_rows["Target"] or 0)
    buyprice = float(selected_rows["Entry_Price"] or 0) 
    sellprice = float(selected_rows["Close_Price"] or 0)

    # stock_data=get_stock_data(ticker,buy_date,end)
    
    # data['data'].to_csv("./output.csv", index=False)

with control_container:
    
    if st.button('Add row', type="primary"):
        add_df = pd.read_csv("./extrarow.csv")
        df = pd.concat([df, add_df], ignore_index=True)
        df.to_csv("./data.csv", index=False)
        
    selected_date = st.date_input(
        "Select time period",
        (datetime.datetime.strptime(buy_date,"%Y-%m-%d"), datetime.datetime.strptime(end,"%Y-%m-%d")),
        max_value=datetime.datetime.now(),
        format="MM.DD.YYYY"
    )

    if len(selected_date) == 2:
        # st.write("You selected:", selected_date)    
        stock_data=get_stock_data(ticker,selected_date[0] - datetime.timedelta(days=100),selected_date[1] + datetime.timedelta(days=100))

        with chart_container:
            create_chart(stock_data,buy_date,buyprice,stop,target,sell_date,sellprice)
