import numpy as np
import pandas as pd
import yfinance as yf

def histVaR(y, s=None, e=None, VaR=95, log_returns=True):
    p = pd.DataFrame()  # Create an empty DataFrame

    # Loop for data extraction & Set up statements for start and end dates
    for ticker in y:
        if s is None and e is None:
            # When neither start date nor end date is defined
            data = yf.download(ticker, start="2007-01-01")
        elif e is None:
            data = yf.download(ticker, start=s) # Only start date is defined
        elif s is None:
            data = yf.download(ticker, end=e)  # When only end date is defined
        else:
            # When both start date and end date are defined
            data = yf.download(ticker, start=s, end=e)

        # Extract the Adjusted Close prices and add to the DataFrame
        if not data.empty:
            p[ticker] = data[('Close', f'{ticker}')]

    p = p.dropna() # Drop rows with NA values
    
    p.columns = y
  
    data = p
      
    # Check if there are less than 100 observations
    if len(data) < 100:
      print("Insufficient number of observations.")
      return None
      
    # Calculate log returns if log_returns is True
    if log_returns:
      data = np.log(data / data.shift(1)).dropna()  # Log returns
      
    # Calculate the historical VaR (quantile of the distribution)
    var_values = data.apply(
      lambda col: np.percentile(col, 100 - VaR), 
      axis=0
      )
      
    # Convert to a DataFrame to display results
    var_df = pd.DataFrame(var_values)
    var_df.columns = [f"VaR {VaR}%"]
      
    return var_df
  
histVaR(y=["MU", "C"])
