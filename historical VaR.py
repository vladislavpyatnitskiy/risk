import numpy as np
import pandas as pd

def histVaR(data, VaR, log_returns=True):
    """
    Calculate Value at Risk (VaR) via Historical Method.
    
    :param data: A DataFrame or NumPy array of stock price data.
    :param VaR: The desired confidence level for VaR (e.g., 95 for 95% VaR).
    :param log_returns: Whether to calculate log returns (True by default).
    :return: A NumPy array or DataFrame with the VaR values.
    """
    
    # Check if there are less than 100 observations
    if len(data) < 100:
        print("Insufficient number of observations.")
        return None
    
    # Calculate log returns if log_returns is True
    if log_returns:
        data = np.log(data / data.shift(1)).dropna()  # Log returns
    
    # Calculate the historical VaR (quantile of the distribution)
    var_values = data.apply(lambda col: np.percentile(col, 100 - VaR), axis=0)
    
    # Convert to a DataFrame to display results
    var_df = pd.DataFrame(var_values)
    var_df.columns = [f"VaR {VaR}%"]
    
    return var_df

# Test with stock data
# Example: stock_data is assumed to be a DataFrame with columns of stock prices
# stock_data = pd.read_csv('your_data.csv')
# Test
histVaR(result, 95)
