import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode

# Sample data
data = {
    'row_labels': [101, 102, 103, 104, 105, 106, 107],
    'ticker': ['Xavier', 'Ann', 'Jana', 'Yi', 'Robin', 'Amal', 'Nori'],
    'city': ['Mexico City', 'Toronto', 'Prague', 'Shanghai', 'Manchester', 'Cairo', 'Osaka'],
    'age': [41, 28, 33, 34, 38, 31, 37],
    'py-score': [88.0, 79.0, 81.0, 80.0, 68.0, 61.0, 84.0]
}

df = pd.DataFrame(data)

# Configure the grid
gb = GridOptionsBuilder.from_dataframe(df[['row_labels', 'ticker']])
gb.configure_selection(selection_mode='single', use_checkbox=True)

gb.configure_default_column(editable=True)
gb.configure_column("row_labels", editable=False)
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
st.dataframe(selected_rows)
st.write(selected_rows.iloc[0]["ticker"])
