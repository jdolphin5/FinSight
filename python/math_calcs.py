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

def calculate_rsi(df, periods=14):
    # Calculate the price changes (delta)
    delta = df['close'].diff()

    # Separate gains and losses
    gain = (delta.where(delta > 0, 0))
    loss = (-delta.where(delta < 0, 0))

    # Calculate the average gain and average loss using rolling mean
    avg_gain = gain.rolling(window=periods, min_periods=1).mean()
    avg_loss = loss.rolling(window=periods, min_periods=1).mean()

    # Avoid division by zero (if avg_loss is 0)
    rs = avg_gain / avg_loss.replace(0, 1e-10)  # Replace 0 to avoid division by zero

    # Calculate the RSI
    rsi = 100 - (100 / (1 + rs))

    # Add RSI to the dataframe
    df['RSI'] = rsi
    
    return df

def calculate_stochastic_oscillator(df, period=14):
    """
    Calculate the Stochastic Oscillator (%K) for a given DataFrame.

    :param df: DataFrame containing 'close', 'high', and 'low' columns.
    :param period: The look-back period for calculating %K (default is 14).
    :return: DataFrame with an added 'stochastic_k' column.
    """
    df = df.copy()  # Make a copy of the DataFrame

    # Calculate the rolling lowest low and highest high for the look-back period
    df['lowest_low'] = df['low'].rolling(window=period).min()
    df['highest_high'] = df['high'].rolling(window=period).max()

    # Calculate the %K value (Stochastic Oscillator)
    df['stochastic_k'] = 100 * (df['close'] - df['lowest_low']) / (df['highest_high'] - df['lowest_low'])

    # Drop NaN values (which arise from the initial period where rolling window is not full)
    df.dropna(subset=['stochastic_k'], inplace=True)

    return df

def calculate_cci(df, period=20):
    """
    Calculate the Commodity Channel Index (CCI) for a given DataFrame.

    :param df: DataFrame containing 'close', 'high', and 'low' columns.
    :param period: The look-back period for calculating CCI (default is 20).
    :return: DataFrame with an added 'CCI' column.
    """
    df = df.copy()  # Make a copy of the DataFrame
    
    # Calculate the Typical Price (TP)
    df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
    
    # Calculate the SMA of Typical Price
    df['sma_typical_price'] = df['typical_price'].rolling(window=period).mean()
    
    def mean_deviation(typical_price_series):
        sma_tp = typical_price_series.mean()  # SMA of the typical price over the window
        return ((typical_price_series - sma_tp).abs()).mean()  # Mean of absolute deviations
    
    df['mean_deviation'] = df['typical_price'].rolling(window=period).apply(mean_deviation)
    
    # Calculate the CCI
    df['CCI'] = (df['typical_price'] - df['sma_typical_price']) / (0.015 * df['mean_deviation'])
    
    # Drop NaN values (which arise from the initial period where rolling window is not full)
    df.dropna(subset=['CCI'], inplace=True)
    
    return df

def calculate_bollinger_bands(df, period=20):
    """
    Calculate Bollinger Bands for a given DataFrame.

    :param df: DataFrame containing 'close' prices.
    :param period: The look-back period for calculating the middle band (SMA) and standard deviation (default is 20).
    :return: DataFrame with added 'Middle Band', 'Upper Band', and 'Lower Band' columns.
    """
    df = df.copy()  # Make a copy of the DataFrame
    
    # Calculate the Middle Band (SMA)
    df['Middle Band'] = df['close'].rolling(window=period).mean()
    
    # Calculate the rolling standard deviation of the closing prices
    df['StdDev'] = df['close'].rolling(window=period).std()
    
    # Calculate the Upper and Lower Bands
    df['Upper Band'] = df['Middle Band'] + (2 * df['StdDev'])
    df['Lower Band'] = df['Middle Band'] - (2 * df['StdDev'])
    
    # Drop NaN values that arise from the initial period where the rolling window is incomplete
    df.dropna(subset=['Middle Band', 'Upper Band', 'Lower Band'], inplace=True)
    
    return df

def calculate_atr(df, period=14):
    """
    Calculate the Average True Range (ATR) for a given DataFrame.

    :param df: DataFrame containing 'high', 'low', and 'close' columns.
    :param period: The look-back period for calculating the ATR (default is 14).
    :return: DataFrame with added 'TR' and 'ATR' columns.
    """
    df = df.copy()  # Make a copy of the DataFrame

    # Calculate the True Range (TR)
    df['prev_close'] = df['close'].shift(1)
    df['high_low'] = df['high'] - df['low']
    df['high_prev_close'] = (df['high'] - df['prev_close']).abs()
    df['low_prev_close'] = (df['low'] - df['prev_close']).abs()

    # True Range is the maximum of (high-low), |high-previous close|, |low-previous close|
    df['TR'] = df[['high_low', 'high_prev_close', 'low_prev_close']].max(axis=1)

    # Calculate the ATR using the Exponential Moving Average (EMA) of True Range
    df['ATR'] = df['TR'].ewm(span=period, adjust=False).mean()

    # Drop the helper columns to clean up the DataFrame
    df.drop(['prev_close', 'high_low', 'high_prev_close', 'low_prev_close'], axis=1, inplace=True)

    return df