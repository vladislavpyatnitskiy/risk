import numpy as np
import pandas as pd
import yfinance as yf

def Rachev_ratio(y, s=None, e=None, VaR=95, log_returns=True):
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
  
    # Check if there are fewer than 100 observations
    if len(p) < 100:
        print("Error. Insufficient number of observations.")
        return
    
    # Calculate log returns if requested and remove NA values
    if log_returns:
        p = np.log(p / p.shift(1)).dropna()
    
    L = pd.DataFrame(index=p.columns)  # Initialize with asset names as index
    
    # Loop over VaR values
    for m in range(len(VaR)):
        rachev = []
        
        # Loop over columns (assets) in x
        for col in p.columns:
            es = p[col].sort_values()  # Sort in ascending order
            
            # Calculate Rachev ratio
            lower_tail = es.iloc[:int((1 - VaR[m] * 0.01) * len(es))]
            upper_tail = es.iloc[int(VaR[m] * 0.01 * len(es)):]
            
            #rachev_ratio = round(upper_tail.mean() / -lower_tail.mean(), 3)
            rachev.append(round(upper_tail.mean() / -lower_tail.mean(), 3))
        
        L[f"Rachev Ratio at {VaR[m]}%"] = rachev
    
    return L

Rachev_ratio(
  y=["UNM", "AIG", "OMF", "MET", "HIG"], s="2022-01-01", 
  VaR=[95, 97.5, 99]
  )
