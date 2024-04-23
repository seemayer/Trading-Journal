from functions import *
from streamlit_lightweight_charts import renderLightweightCharts

def create_chart(stock_data,start,buyprice,stop,target,sell_date,sellprice):
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
