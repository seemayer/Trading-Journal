import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

# Create a sample DataFrame with columns A and B
data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)

# Define a custom function to calculate the product of A and B
def calculate_product(row):
    return row['A'] * row['B']

# Add a new column 'Product' with the calculated values
df['Product'] = df.apply(calculate_product, axis=1)

# Display the AG Grid
grid_return = AgGrid(df, editable=True, key='my_grid')

# Get the edited DataFrame from the grid
edited_df = grid_return['data']

# Update the 'Product' column based on the edited values
edited_df['Product'] = edited_df.apply(calculate_product, axis=1)

# Display the updated DataFrame
st.write("Updated DataFrame:")
st.write(edited_df)
