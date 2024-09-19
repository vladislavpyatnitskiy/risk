import numpy as np
import pandas as pd
from scipy.stats import norm

def CVaR_VC(x, es=95, log_returns=True):
    # Check whether there are less than 100 observations
    if len(x) < 100:
        print("Insufficient number of observations.")
        return
    
    # Calculate log returns if requested and remove NAs
    if log_returns:
        x = np.log(x / x.shift(1)).dropna()
    
    v = x.apply([np.mean, np.std], axis=0) # Means & Standard Deviations
    
    l = [] # Set up list to contain future values
    
    # Calculate VaR using standard normal probabilities
    for col in x.columns:
        MEAN = v.loc['mean', col]
        SD = v.loc['std', col]
        l.append(MEAN - (norm.pdf(norm.ppf(es * .01)) / (1 - es * .01)) * SD)
    
    # Return DataFrame with CVaR values
    return pd.DataFrame(l, index=x.columns, columns=[f"ES VC {es}%"])

# Example usage:
# Assuming stock_data is a pandas DataFrame with price data
# stock_data = pd.read_csv("your_data.csv")
CVaR_VC(result, 95)
