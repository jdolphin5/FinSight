from flask import Flask, jsonify
from dash import Dash, html, dcc, Input, Output
import requests
import pandas as pd  # Import pandas for data manipulation
from datetime import datetime
from calculations.math_calcs import calculate_wma
from visualisation.figures import generate_figures
from util.date_time import compute_time_frame

# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app with Flask server
app = Dash(__name__, server=server)

colours = {
    'background': '#FAFAFA',
    'text': '#111827',
    'button-bg1': '#3C83F6',
    'button-text1': '#FFFFFF',
    'button-bg2': '#F0F6FF',
    'button-text2': '#7083F7'
}

# Example stock codes for dropdown
available_stocks = ['AAPL', 'AMZN', 'GOOGL', 'TSLA', 'MSFT']
available_graph_types = ['Standard / OHLC', 'EMA - Exponential Moving Average', 'MACD - Moving Average Convergence/Divergence', 'ADX - Average Directional Index', 'Parabolic SAR - Stop and Reverse',
                         'RSI - Relative Strength Index', '%K - Stochastic Oscillator', 'CCI - Commodity Channel Index',
                         'Bollinger Bands', 'ATR - Average True Range']

# Define the Dash layout
app.layout = html.Div([
    html.H1("Stock Data Visualisation"),

    # Dropdown to select stock code
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': stock, 'value': stock} for stock in available_stocks],
        value='AAPL',  # Default value
        placeholder='Select Stock'
    ),

    dcc.Dropdown(
        id='graph-type-dropdown',
        options=[{'label': graph_type, 'value': graph_type} for graph_type in available_graph_types],
        value='Standard / OHLC',
        placeholder='Select Graph Type'
    ),

    html.Br(),
    dcc.Graph(id='stock-graph'),

    # Buttons for time range selection
    html.Div([
        html.Button('5 Years', id='5-years-button', n_clicks_timestamp=None, style={'background-color': colours['button-bg1'], 'color': colours['button-text1']}),
        html.Button('1 Year', id='1-year-button', n_clicks_timestamp=None, style={'background-color': colours['button-bg1'], 'color': colours['button-text1']}),
        html.Button('6 Months', id='6-months-button', n_clicks_timestamp=None, style={'background-color': colours['button-bg1'], 'color': colours['button-text1']}),
        html.Button('1 Month', id='1-month-button', n_clicks_timestamp=None, style={'background-color': colours['button-bg1'], 'color': colours['button-text1']}),
        html.Button('5 Days', id='5-days-button', n_clicks_timestamp=None, style={'background-color': colours['button-bg1'], 'color': colours['button-text1']}),
        html.Button('1 Day', id='1-day-button', n_clicks_timestamp=None, style={'background-color': colours['button-bg1'], 'color': colours['button-text1']}),
    ], style={'display': 'flex', 'gap': '10px', 'margin': '10px 0'}),
    html.Br(),
    html.Div(id='asterix-info'),
    html.Div(id='stock-info'),
    html.Div(id='simple-moving-average'),
    html.Div(id='weighted-moving-average'),

], style={'color': colours['text'], 'background-color': colours['background'], 'font-family': 'Arial', 'padding': '0px 10px 0px 10px'})

@app.callback(
    [Output('stock-graph', 'figure'), Output('asterix-info', 'children'), Output('stock-info', 'children'), Output('simple-moving-average', 'children'), Output('weighted-moving-average', 'children')],
    [Input('stock-dropdown', 'value'),
     Input('graph-type-dropdown', 'value'),
     Input('5-years-button', 'n_clicks_timestamp'),
     Input('1-year-button', 'n_clicks_timestamp'),
     Input('6-months-button', 'n_clicks_timestamp'),
     Input('1-month-button', 'n_clicks_timestamp'),
     Input('5-days-button', 'n_clicks_timestamp'),
     Input('1-day-button', 'n_clicks_timestamp'),
     Input('stock-graph', 'relayoutData')]
)
def update_graph(selected_stock, selected_graph_type, ts_5y, ts_1y, ts_6m, ts_1m, ts_5d, ts_1d, relayoutData):
    # Determine the selected time range based on the button clicks

    # Initialize the time range to 'Default'
    time_range = 'Default'

    # Create a dictionary to track timestamps
    timestamps = {
        '5y': ts_5y,
        '1y': ts_1y,
        '6m': ts_6m,
        '1m': ts_1m,
        '5d': ts_5d,
        '1d': ts_1d
    }

    # Filter out None or zero values (indicating no clicks)
    valid_timestamps = {k: v for k, v in timestamps.items() if v is not None and v > 0}

    # Find the button with the most recent timestamp (i.e., the highest value)
    if valid_timestamps:
        most_recent = max(valid_timestamps, key=valid_timestamps.get)

        # Based on which button was clicked most recently, set the time range
        if most_recent == '5y':
            time_range = '5y'
        elif most_recent == '1y':
            time_range = '1y'
        elif most_recent == '6m':
            time_range = '6m'
        elif most_recent == '1m':
            time_range = '1m'
        elif most_recent == '5d':
            time_range = '5d'
        elif most_recent == '1d':
            time_range = '1d'

    time_range_from, time_range_to = compute_time_frame(time_range, datetime.now())

    # Build the URL for the GET request to the backend
    backend_url = f"http://127.0.0.1:8080/stocks/datefrom/{time_range_from}/dateto/{time_range_to}/code/{selected_stock}"

    # Make a GET request to fetch stock data from the backend
    try:
        response = requests.get(backend_url)
        response.raise_for_status()  # Check if request was successful
        stock_data = response.json()
    except requests.exceptions.RequestException as e:
        return {}, f"Error fetching data: {str(e)}"

    # Check if stock_data is valid and has the necessary structure
    if not stock_data or not isinstance(stock_data, list):
        return {}, "No data available or invalid format"

    # Convert the stock data to a Pandas DataFrame
    df = pd.DataFrame(stock_data)

    # Ensure the 'local_time' column is in datetime format
    # Convert from UTC+0 in DB to UTC+8 (US/East Timezone) 
    df['local_time'] = pd.to_datetime(df['local_time']).dt.tz_convert('US/Eastern')
    
    df_filtered = df
    df_filtered = df_filtered.copy()

    if relayoutData and 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
        # Extract the uniform x-range (indices) from relayoutData
        start_idx = int(float(relayoutData['xaxis.range[0]']))  # relayoutData returns strings, so cast to float first
        end_idx = int(float(relayoutData['xaxis.range[1]']))

        # Ensure indices are within bounds
        start_idx = max(0, start_idx)
        end_idx = min(len(df_filtered) - 1, end_idx)

        # Map the indices back to the corresponding timestamps
        start_time = df_filtered['local_time'].iloc[start_idx]
        end_time = df_filtered['local_time'].iloc[end_idx]

        # Filter the DataFrame based on these time values
        df_filtered = df[(df['local_time'] >= start_time) & (df['local_time'] <= end_time)]

        # Safely copy the DataFrame
        df_filtered = df_filtered.copy()

    stock_times = df_filtered['local_time']  # Using the DataFrame column
    stock_close_prices = df_filtered['close']  # Using the DataFrame column

    asterix_info, figure = generate_figures(df_filtered, selected_graph_type, selected_stock, stock_times, stock_close_prices, time_range)

    # Stock information (showing the last close price and time)
    last_entry = df_filtered.iloc[-1] if not df_filtered.empty else {}
    stock_code = last_entry.get('code', 'N/A')
    last_close_price = last_entry.get('close', 0)
    last_time = last_entry.get('local_time', 'N/A')
    info = f"Stock: {stock_code}, Last close price: {last_close_price}, Time: {last_time}"

    sma_total = 0

    for close in stock_close_prices:
        sma_total += close
    
    if (len(stock_close_prices > 0)):
        sma = sma_total / len(stock_close_prices)
    else:
        sma = 0

    sma_info = f"SMA (Simple Moving Average) for {len(stock_close_prices)} points is {round(sma, 3)}"

    period = len(df_filtered['close']) # Weighted moving average period equal to number of data points
    df_filtered['WMA'] = calculate_wma(df_filtered, period)

    wma = df_filtered['WMA'].iloc[-1]

    wma_info = f'WMA (Weighted Moving Average) for {len(df_filtered['close'])} points is {round(wma, 3)}'

    return figure, asterix_info, info, sma_info, wma_info


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
