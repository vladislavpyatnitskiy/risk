import numpy as np
import pandas as pd
from scipy.stats import norm

def VaR_VC(data, VaR=95, log_returns=True):
    """
    Calculate Value at Risk (VaR) via Variance-Covariance Method.
    
    :param data: A DataFrame or NumPy array of stock price data.
    :param VaR: The desired confidence level for VaR (e.g., 95 for 95% VaR).
    :param log_returns: Whether to calculate log returns (True by default).
    :return: A DataFrame with VaR values.
    """
    
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

# Test with stock data
# Example: stock_data is assumed to be a DataFrame with columns of stock prices
# stock_data = pd.read_csv('your_data.csv')
VaR_VC(result, 95)
