import numpy as np
import pandas as pd
import yfinance as yf

def histCVaR(y, s=None, e=None, CVaR=95, log_returns=True):
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
        print("Error. Insufficient number of observations.")
        return None
    
    # Calculate log returns if log_returns is True
    if log_returns:
        data = np.log(data / data.shift(1)).dropna()  # Log returns
    
    ES = [] # Initialize an empty list to store CVaR values
    
    # Loop through each column (asset) in the DataFrame
    for col in data.columns:
        sorted_returns = data[col].sort_values(ascending=True)  # Sort returns
        
        # Select the worst (1 - CVaR%) returns and calculate their mean
        cutoff = int((1-CVaR*.01)*len(sorted_returns))
        worst_returns = sorted_returns.iloc[:cutoff]
        
        # Calculate the mean of the worst returns (Expected Shortfall)
        ES.append(worst_returns.mean())
    
    # Create a DataFrame to display CVaR values for each column
    return pd.DataFrame(ES, index=data.columns, columns=[f"CVaR {CVaR}%"])

histCVaR(y=["UNM", "AIG", "OMF", "MET", "HIG"], s="2022-01-01")
