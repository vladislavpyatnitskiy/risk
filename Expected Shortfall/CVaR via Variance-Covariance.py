import numpy as np
import pandas as pd
from scipy.stats import norm
import yfinance as yf

def CVaR_VC(y, s=None, e=None, es=95, log_returns=True):
    
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
  
    # Check whether there are less than 100 observations
    if len(p) < 100:
        print("Insufficient number of observations.")
        return
    
    # Calculate log returns if requested and remove NAs
    if log_returns:
        p = np.log(p / p.shift(1)).dropna()
    
    v = p.apply([np.mean, np.std], axis=0) # Means & Standard Deviations
    
    l = [] # Set up list to contain future values
    
    # Calculate VaR using standard normal probabilities
    for col in p.columns:
        MEAN = v.loc['mean', col]
        SD = v.loc['std', col]
        l.append(MEAN - (norm.pdf(norm.ppf(es * .01)) / (1 - es * .01)) * SD)
    
    # Return DataFrame with CVaR values
    return pd.DataFrame(l, index=p.columns, columns=[f"ES VC {es}%"])

CVaR_VC(y=["UNM", "AIG", "OMF", "MET", "HIG"], s="2022-01-01")
