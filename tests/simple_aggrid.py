import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode

# Sample data
data = {
    'row_labelsrow_labelsrow_labelsrow_labels': [101, 102, 103, 104, 105, 106, 107],
    'ticker': ['Xavier', 'Ann', 'Jana', 'Yi', 'Robin', 'Amal', 'Nori'],
    'city': ['Mexico City', 'Toronto', 'Prague', 'Shanghai', 'Manchester', 'Cairo', 'Osaka'],
    'age': [41, 28, 33, 34, 38, 31, 37],
    'py-score': [88.0, 79.0, 81.0, 80.0, 68.0, 61.0, 84.0]
}

df = pd.DataFrame(data)

# Configure the grid
gb = GridOptionsBuilder.from_dataframe(df[['row_labelsrow_labelsrow_labelsrow_labels', 'ticker']])

# https://www.ag-grid.com/angular-data-grid/column-sizing/#auto-size-columns-to-fit-cell-contents
gb.configure_grid_options(autoSizeStrategy={'type':'fitCellContents','skipHeader':True})
gb.configure_column(field='ticker',width=5)
gridOptions = gb.build()


# Display the grid
data = AgGrid(df, gridOptions=gridOptions)


