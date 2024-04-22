import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import datetime
import yfinance as yf
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode, JsCode
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

df = pd.read_csv("./data.csv")

st.subheader("Data Toggling for an Area Chart and Candlestick")

control_container = st.container(border=True)
chart_container = st.container(border=True)
table_container = st.container(border=True)


number_formatter = JsCode("""
    function(params) {
        return (params.value == null) ? params.value : "£"+params.value.toLocaleString("en-US", { maximumFractionDigits: 2, minimumFractionDigits: 2 }); 
    }
    """)

r_formatter = JsCode("""
    function(params) {
        return (params.value == null) ? params.value : params.value.toLocaleString("en-US", { maximumFractionDigits: 1, minimumFractionDigits: 1 }); 
    }
    """)

v_getter = JsCode("""
   
    function(params) {
         
        if (params.data.Close_Price) {
            var output = (params.data.Close_Price - params.data.Entry_Price)*params.data.Pounds_Per_Point
        } else {
            return;
        }
        
        // write to the data to aggrid
        var col = params.colDef.field;
        params.data[col] = output;

        return output;                  
        
    }
    
    """)


with table_container:
    # Configure the grid
 
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode='single', use_checkbox=False )
    gb.configure_default_column(editable=True)
    #Define calculated columns
    gb.configure_column(field='Position_Size', valueGetter='data.Pounds_Per_Point * data.Entry_Price', type=['numericColumn'],cellStyle={'background-color': 'aliceblue'}, valueFormatter=number_formatter)
    gb.configure_column(field='Margin', valueGetter= 'getValue("Position_Size") * .25', type=['numericColumn'],cellStyle={'background-color': 'aliceblue'}, valueFormatter=number_formatter)
    gb.configure_column(field='Monetary_Risk', valueGetter='(data.Entry_Price - data.Stop)*data.Pounds_Per_Point', type=['numericColumn'],cellStyle={'background-color': 'aliceblue'}, valueFormatter=number_formatter)
    gb.configure_column(field='P/L', valueGetter=v_getter, type=['numericColumn'],cellStyle={'background-color': 'aliceblue'}, valueFormatter=number_formatter)
    gb.configure_column(field='R:R_plan', valueGetter='(data.Target - data.Entry_Price)/(data.Entry_Price - data.Stop)', type=['numericColumn'],cellStyle={'background-color': 'aliceblue'}, valueFormatter=r_formatter)
    gb.configure_side_bar()
    gridOptions = gb.build()

    # Display the grid
    data = AgGrid(df, gridOptions=gridOptions,
                editable=True, 
                enable_enterprise_modules=True, 
                allow_unsafe_jscode=True, 
                update_mode=GridUpdateMode.VALUE_CHANGED | GridUpdateMode.SELECTION_CHANGED, 
                columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
                )

    # Process selected row
    selected_rows = data['selected_rows']
    # st.dataframe(data['selected_rows'])

    ticker = selected_rows.iloc[0]["Ticker"]
    start = convertdatestring(selected_rows.iloc[0]["Date"])
    end = adddaystodatestring(convertdatestring(selected_rows.iloc[0]["Date"]),100)
    sell_date = selected_rows.iloc[0]["Close_Date"]
    if sell_date:
        sell_date=convertdatestring(sell_date)
        end=sell_date
        

    stop = selected_rows.iloc[0]["Stop"].astype(float) #must be float otherwise renderlightweightcharrs does not like it
    target = selected_rows.iloc[0]["Target"].astype(float) #must be float otherwise renderlightweightcharrs does not like it
    buyprice = selected_rows.iloc[0]["Entry_Price"].astype(float) #must be float otherwise renderlightweightcharrs does not like it
    sellprice = selected_rows.iloc[0]["Close_Price"]
    if sellprice: #only convert if sellprice exists
        sellprice = sellprice.astype(float)

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
