import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

d= {"Type":["Notebook","DVDs"],"Quantity":[1,2],'Price':[400,200]}
df = pd.DataFrame(d)
response = AgGrid(df,editable=True)
st.bar_chart(response["data"],x='Type',y='Price')