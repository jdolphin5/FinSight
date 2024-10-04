import pandas as pd
import numpy as np

def calculate_wma(df, period):
    """
    Calculate the Weighted Moving Average (WMA) for a given period.
    
    Args:
    - df (pd.DataFrame): DataFrame with stock price data.
    - period (int): The number of days to calculate the WMA for.
    
    Returns:
    - pd.Series: Weighted Moving Average.
    """
    weights = pd.Series(range(1, period + 1))  # Create a range of weights (1 to period)

    wma = df['close'].rolling(window=period).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    
    return wma

def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    df['EMA_12'] = df['close'].ewm(span=short_period, adjust=False).mean()
    df['EMA_26'] = df['close'].ewm(span=long_period, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
    return df

def calculate_true_range(df):
    df['TR'] = np.maximum(df['high'] - df['low'], 
                          np.maximum(abs(df['high'] - df['close'].shift(1)), 
                                     abs(df['low'] - df['close'].shift(1))))
    return df

def calculate_dm(df):
    df['DM+'] = np.where((df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']), 
                         np.maximum(df['high'] - df['high'].shift(1), 0), 0)
    df['DM-'] = np.where((df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)), 
                         np.maximum(df['low'].shift(1) - df['low'], 0), 0)
    return df

def calculate_di(df, period):
    df['DI+'] = 100 * (df['DM+'].rolling(window=period).sum() / df['TR'].rolling(window=period).sum())
    df['DI-'] = 100 * (df['DM-'].rolling(window=period).sum() / df['TR'].rolling(window=period).sum())
    return df

def calculate_adx(df, period):
    df['DX'] = 100 * (abs(df['DI+'] - df['DI-']) / (df['DI+'] + df['DI-']))
    df['ADX'] = df['DX'].ewm(span=period, min_periods=period).mean()
    return df

def calculate_parabolic_sar(df, initial_af=0.02, max_af=0.20, step_af=0.02):
    # Initialize SAR values
    sar = df['low'][0]  # Starting SAR for uptrend
    trend_up = True  # Start with an uptrend assumption
    ep = df['high'][0]  # Extreme Point (EP) starts as the highest price in uptrend
    af = initial_af  # Acceleration Factor (AF) starts at 0.02
    
    # Initialize lists to store SAR values and trend direction
    sar_values = [sar]
    
    for i in range(1, len(df)):
        prev_sar = sar
        prev_ep = ep
        
        if trend_up:
            # Uptrend: calculate SAR
            sar = prev_sar + af * (ep - prev_sar)
            
            # Adjust SAR to not be higher than the last two lows
            sar = min(sar, df['low'][i], df['low'][i - 1])
            
            # If new high is reached, update EP and increase AF
            if df['high'][i] > ep:
                ep = df['high'][i]
                af = min(af + step_af, max_af)
            
            # If SAR crosses below price (reversal), switch to downtrend
            if df['low'][i] < sar:
                trend_up = False
                sar = ep  # Reset SAR to EP
                ep = df['low'][i]  # Reset EP to lowest price of new trend
                af = initial_af  # Reset AF
        else:
            # Downtrend: calculate SAR
            sar = prev_sar - af * (prev_sar - ep)
            
            # Adjust SAR to not be lower than the last two highs
            sar = max(sar, df['high'][i], df['high'][i - 1])
            
            # If new low is reached, update EP and increase AF
            if df['low'][i] < ep:
                ep = df['low'][i]
                af = min(af + step_af, max_af)
            
            # If SAR crosses above price (reversal), switch to uptrend
            if df['high'][i] > sar:
                trend_up = True
                sar = ep  # Reset SAR to EP
                ep = df['high'][i]  # Reset EP to highest price of new trend
                af = initial_af  # Reset AF
        
        # Store SAR value for this iteration
        sar_values.append(sar)
    
    df['SAR'] = sar_values
    return df