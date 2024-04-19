import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

# Create a DataFrame
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [4, 5, 6]
})

# Define grid options
grid_options = {
    "defaultColDef": [
        
    ],
    
    
    
    
    
    "columnDefs": [
        {
            "field": "a",
            
        },
        {"field": "b" },
        {
            "field": "Total",
            "valueGetter": "data.a + data.b"
        },
        {
            "field": "Total x 2",
            "valueGetter": "getValue('Total') * 2"
        }
        
 ]
}

# Display the grid
response = AgGrid(
    df,
    editable=True,
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
