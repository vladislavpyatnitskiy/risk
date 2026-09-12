import numpy as np
import pandas as pd
from scipy.stats import norm
import yfinance as yf

def VaR_VC(y, s=None, e=None, VaR=95, log_returns=True):
    
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
    
    # Calculate means and standard deviations of the log returns
    MEAN = data.mean()
    SD = data.std()
    
    # Set up an empty DataFrame to store VaR values
    var_values = pd.DataFrame(index=data.columns, columns=[f"VaR VC {VaR}%"])
    
    # Calculate VaR using the Z-score from the normal distribution
    z_score = norm.ppf(1 - VaR * 0.01)  
    
    # Calculate VaR for each asset
    for col in data.columns:
        var_values.loc[col, f"VaR VC {VaR}%"] = MEAN[col] + z_score * SD[col]
    
    return var_values

VaR_VC(y=["UNM", "AIG", "OMF", "MET", "HIG"], s="2022-01-01")
