import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid

# Example data
data = {
    'Country': ['Norway', 'Russia', 'China', 'Japan'],
    'Capital': ['Oslo', 'Moscow', 'Beijing', 'Tokyo'],
    'Population (Millions)': [5.4, 144.5, 1400, 126.5]
}
df = pd.DataFrame(data)

# Configure the column format
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column("Population (Millions)", cellStyle={"fontWeight": "bold",'background-color': 'aliceblue'})

# Create an AgGrid
AgGrid(df, height=400, gridOptions=gb.build())
