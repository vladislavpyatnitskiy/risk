import numpy as np
import pandas as pd

def histCVaR(data, CVaR, log_returns=True):
    """
    Calculate Expected Shortfall (CVaR) via Historical Method.
    
    :param data: A DataFrame or NumPy array of stock price data.
    :param CVaR: The desired confidence level for CVaR (e.g., 95 for 95% CVaR).
    :param log_returns: Whether to calculate log returns (True by default).
    :return: A DataFrame with CVaR values for each column (asset).
    """
    
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

# Test with stock data
# Example: stock_data is assumed to be a DataFrame with columns of stock prices
# stock_data = pd.read_csv('your_data.csv')
histCVaR(result, 95, True)
