import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

# Create a DataFrame
df = pd.DataFrame({
    'col1': [1, 2, 3],
    'col2': [4, 5, 6],
    'col3': [7, 8, 9]
})

# Define grid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True)  # Make columns editable by default

# Define the calculated column using an expression
gb.configure_column('col1', type=['numericColumn'])
gb.configure_column('col2', type=['numericColumn'])
gb.configure_column('col3', valueGetter='data.col1 + data.col2',valueSetter='(params: ValueSetterParams) => params.data.col3 = params.newValue')



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
new_df = response['data']
st.dataframe(new_df)
