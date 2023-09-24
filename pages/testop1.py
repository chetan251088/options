import streamlit as st
import pandas as pd
import requests
import time

import json
    


# Function to fetch option chain data from the API
def fetch_option_chain_data():
    # Make an API request to fetch the data
    response = requests.get("https://mksapi.kotaksecurities.com/60newserviceapi/cmots/derivative/option-chain/i/eyJzeW1ib2wiOiAiQkFOS05JRlRZIiwgImV4cGlyeWRhdGUiOiAiMjAtU2VwLTIwMjMifQ==")  # Replace "API_URL_HERE" with the actual API URL

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        # Handle error cases
        st.error("Error fetching option chain data from the API")
# Assuming 'api_data' contains the JSON response

# Streamlit app
def main():
    st.title("Option Chain Data")
    key = None
    value = None
    df = pd.DataFrame(fetch_option_chain_data())
    # Create a list of unique values for the "pSymbol" column
    symbols = df['strikeprice'].unique()
    # Create a dropdown menu to select the symbol
    selected_symbol = st.selectbox(label='Select Symbol', options=symbols)
    # Filter the dataframe based on the selected symbol
    filtered_df = df[df['strikeprice'] == selected_symbol]

    # Display the filtered dataframe
    st.write(filtered_df)
    # Add a search bar to search for specific strike prices
    search_bar = st.text_input(label='Search Strike Price', placeholder='Enter strike price here...')

    # Search for the entered strike price in the filtered dataframe
    if search_bar != '':
        searched_df = filtered_df[filtered_df['strikeprice'] == float(search_bar)]
        
        # Display the searched dataframe
        st.write(searched_df)
    else:
        st.write("Please enter a valid strike price")
    # Create an empty dataframe to store the option chain data
    option_chain_df = pd.DataFrame(columns=["Key", "Value"])
    df = pd.DataFrame(columns=["Key", "Value"])
    df = pd.concat([df, pd.DataFrame({"Key": [key], "Value": [value]})])
    # Set a flag to control the infinite loop
    is_running = True

    while is_running:
        # Fetch option chain data from the API
        option_chain_data = fetch_option_chain_data()

        if option_chain_data:
            # Clear the existing dataframe
            option_chain_df = pd.DataFrame(columns=["Key", "Value"])

            # Process the option chain data and add it to the dataframe
            for key, value in option_chain_data.items():
                #option_chain_df = option_chain_df.concat({"Key": key, "Value": value}, ignore_index=True)
                df = pd.concat([df, pd.DataFrame({"Key": [key], "Value": [value]})])
            # Display the option chain data as an interactive table
            st.dataframe(option_chain_df)
        else:
            # Display a message if no data is available
            st.info("No option chain data available")

        # Add a delay before fetching new data (adjust as per your requirements)
        time.sleep(10)  # Fetch new data every 10 seconds

if __name__ == "__main__":
    main()