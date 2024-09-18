import numpy as np
from scipy.stats import norm

def VaR_D(P, C, r, y, f=1, s=1, VaR=95):
    """
    Calculate VaR (Value at Risk) for a bond.
    
    :param P: Principal value of the bond.
    :param C: Coupon rate.
    :param r: Interest rate (discount rate).
    :param y: Number of years (time to maturity).
    :param f: Frequency of payments (default is 1, annual payments).
    :param s: Spread for the VaR calculation (default is 1).
    :param VaR: Confidence level for VaR (default is 95%).
    :param PV: Present value of the coupon payments (optional).
    :param p: Coupon part for the numerator (optional).
    :return: VaR for the bond.
    """
    
    PV = []
    p = []
    
    # Bond Price calculation
    B = P * (C / r * (1 - (1 + r / f) ** -(y * f)) + (1 + r / f) ** -(y * f))
    
    P_ = P * (1 + C / f) / (1 + r / f) ** (y * f) # Principal part
    
    # Calculate Present Value (PV) of coupons and coupon parts
    for n in range(1, int(y * f)): 
      
        PV.append(C * P / f / (1 + r / f) ** (n * f))
        p.append(n * C * P / f / (1 + r / f) ** (n * f))
    
    D = (sum(p[:int(y*f)-1]) + P_*y*f)/(P_ + sum(PV[:int(y*f)-1])) # Duration
    
    return B * norm.ppf(1 - VaR*.01) * (D/(1 + (r - s*.01)/f)) * (r/f) # VaR

VaR_D(1000, 0.1, 0.05, 3, 1, 1) # Test with sample data
