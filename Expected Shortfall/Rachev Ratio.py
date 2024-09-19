import numpy as np
import pandas as pd

def Rachev_ratio(x, VaR, log_returns=True):
    # Check if there are fewer than 100 observations
    if len(x) < 100:
        print("Error. Insufficient number of observations.")
        return
    
    # Calculate log returns if requested and remove NA values
    if log_returns:
        x = np.log(x / x.shift(1)).dropna()
    
    L = pd.DataFrame(index=x.columns)  # Initialize with asset names as index
    
    # Loop over VaR values
    for m in range(len(VaR)):
        rachev = []
        
        # Loop over columns (assets) in x
        for col in x.columns:
            es = x[col].sort_values()  # Sort in ascending order
            
            # Calculate Rachev ratio
            lower_tail = es.iloc[:int((1 - VaR[m] * 0.01) * len(es))]
            upper_tail = es.iloc[int(VaR[m] * 0.01 * len(es)):]
            
            #rachev_ratio = round(upper_tail.mean() / -lower_tail.mean(), 3)
            rachev.append(round(upper_tail.mean() / -lower_tail.mean(), 3))
        
        L[f"Rachev Ratio at {VaR[m]}%"] = rachev
    
    return L

# Example usage:
# Assuming stock_data is a pandas DataFrame with price data
# stock_data = pd.read_csv("your_data.csv")
Rachev_ratio(result, [95, 97.5, 99])
