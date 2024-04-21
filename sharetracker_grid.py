import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

st. set_page_config(layout="wide")

# Create a DataFrame
df = pd.DataFrame({
    'Pounds_Per_Point': [1, 2, 3],
    'Entry_Price': [4, 5, 6],
    'Stop': [4, 5, 6],
    'Target': [4, 5, 6],
})

# Define grid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True)  # Make columns editable by default

# Define the calculated column using an expression

gb.configure_column(field='Position_Size', valueGetter='data.Pounds_Per_Point * data.Entry_Price', type=['numericColumn'])
gb.configure_column(field='Margin', valueGetter= 'getValue("Position_Size") * .25', type=['numericColumn'])
gb.configure_column(field='Monetary Risk', valueGetter='(data.Entry_Price - data.Stop)*data.Pounds_Per_Point', type=['numericColumn'])
gb.configure_column(field='R:R plan', valueGetter='(data.Target - data.Entry_Price)/(data.Entry_Price - data.Stop)', type=['numericColumn'])

grid_options = gb.build()

# Display the grid
response = AgGrid(
    df,
    gridOptions=grid_options,
    height=600,
    width='100%',
    data_return_mode=DataReturnMode.AS_INPUT,
    update_mode=GridUpdateMode.VALUE_CHANGED,
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,  # Set it to True to allow js injection
)

# Get the updated DataFrame
#new_df = response['data']
