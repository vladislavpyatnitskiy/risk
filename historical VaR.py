def histVaR(x, VaR, lg=True):
    """
    Calculate VaR via Historical Method.

    Parameters:
    - x: DataFrame with financial data.
    - VaR: Value at Risk percentage (e.g., 95 for 95% VaR).
    - lg: If True, calculate log returns.

    Returns:
    - DataFrame containing VaR values for each column.
    """

    # Check whether there are less than 100 observations
    if len(x) < 100:
        print("Insufficient number of observations.")
    else:
        if lg:
            x = np.diff(np.log(x), axis=0)[1:]  # log returns and remove NA

        # Calculate historical VaR value and transform into DataFrame format
        VaR_values = np.quantile(x, 1 - VaR * 0.01, axis=0)
        result_df = pd.DataFrame(VaR_values.reshape(1, -1),
                                 columns=[f"VaR {VaR}%"])

        return result_df

# Test
# Assuming stock_data is a DataFrame with financial data
# Make sure to replace stock_data with your actual DataFrame
histVaR(result.iloc[:,1], 99)
