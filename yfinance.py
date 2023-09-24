import yfinance as yf
import time

# Define the security you want to track
security = "AAPL"

# Get the current price of the security
current_price = yf.Ticker(security).info["regularMarketPrice"]

# Set up a streaming connection to receive updates on the security's price
stream = yf.StreamingPrices()
stream.add_symbol(security)

while True:
    # Print the current price every second
    print("Current price:", current_price)
    
    # Update the current price based on the latest update received from the server
    if stream.update():
        current_price = stream.get_latest_price(security)
        
    time.sleep(1)