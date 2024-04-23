import streamlit as st
import pandas as pd

df = pd.read_csv("./data.csv")



edited_df = st.data_editor(df, num_rows="dynamic",width=1000)

if edited_df is not None:
    #favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
    #st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
    edited_df.to_csv("./data.csv", index=False)

if st.button('Save Data'):
    # Your code to save data goes here
    edited_df.to_csv("./data.csv", index=False)
    st.write('Data saved successfully!')




