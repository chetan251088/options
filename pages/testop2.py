import streamlit as st
import requests
import pandas as pd
import numpy as np


# Get the JSON response from the API endpoint
response = requests.get("https://mksapi.kotaksecurities.com/60newserviceapi/cmots/derivative/option-chain/i/eyJzeW1ib2wiOiAiQkFOS05JRlRZIiwgImV4cGlyeWRhdGUiOiAiMjAtU2VwLTIwMjMifQ==")

# Parse the JSON response into a dictionary
data = response.json()

# Convert the dictionary into a pandas DataFrame
df = pd.DataFrame(data["result"])

# Add a dropdown menu to select the key to filter by
keys = ["symbol", "strikeprice", "PutStrikeprice"]
selected_key = st.selectbox("Select Key", options=keys)

# Apply the appropriate filter based on the selected key
if selected_key == "symbol":
    filtered_df = df[df["symbol"].str.startswith("BANKNIFTY")]
elif selected_key == "age":
    filtered_df = df[df["strikeprice"] > 45000]
else:
    filtered_df = df[df["PutStrikeprice"] == 45200]

# Display the filtered data in a table
st.dataframe(filtered_df)