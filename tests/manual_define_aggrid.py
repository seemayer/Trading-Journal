import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

df = pd.DataFrame({'name': [1, 2, 3], 'age': [4, 5, 6]})

columnDefs = [
    { 'field': 'name', 'headerName': 'Name', 'editable': True, 'type':'shaded' },
    { 'field': 'age', 'headerName': 'Age', 'editable': True },
    { 'field': 'total', 'headerName': 'Total', 'valueGetter':'(data.name + data.age)'},
    { 'field': 'totalx2', 'headerName': 'Totalx2', 'valueGetter': 'getValue("total") * 2'},
    # Add more columns as needed
]
defaultColDef = {
    'editable': True,
    'sortable': True,
    'filter': True,
    # Add other default properties here
}
gridOptions = {
    'columnDefs': columnDefs,
    'defaultColDef': defaultColDef,
    # Add other grid options if needed
}




grid_return = AgGrid(df, 
                     editable=True,
                     gridOptions=gridOptions
                     )
new_df = grid_return['data']
