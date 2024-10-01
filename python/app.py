from flask import Flask, jsonify
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import requests
import pandas as pd  # Import pandas for data manipulation

# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app with Flask server
app = Dash(__name__, server=server)

# Example stock codes for dropdown
available_stocks = ['AAPL', 'AMZN', 'GOOGL', 'TSLA', 'MSFT']

# Define the Dash layout
app.layout = html.Div([
    html.H1("Stock Data Visualization"),

    # Dropdown to select stock code
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': stock, 'value': stock} for stock in available_stocks],
        value='AAPL',  # Default value
        placeholder='Select Stock'
    ),

    # Buttons for time range selection
    html.Div([
        html.Button('5 Years', id='5-years-button', n_clicks=0),
        html.Button('1 Year', id='1-year-button', n_clicks=0),
        html.Button('6 Months', id='6-months-button', n_clicks=0),
        html.Button('1 Month', id='1-month-button', n_clicks=0),
        html.Button('5 Days', id='5-days-button', n_clicks=0),
        html.Button('1 Day', id='1-day-button', n_clicks=0),
    ], style={'display': 'flex', 'gap': '10px', 'margin': '10px 0'}),

    dcc.Graph(id='stock-graph'),
    html.Div(id='stock-info'),
    html.Div(id='simple-moving-average'),
    html.Div(id='weighted-moving-average')
])

@app.callback(
    [Output('stock-graph', 'figure'), Output('stock-info', 'children'), Output('simple-moving-average', 'children'), Output('weighted-moving-average', 'children')],
    [Input('stock-dropdown', 'value'),
     Input('5-years-button', 'n_clicks'),
     Input('1-year-button', 'n_clicks'),
     Input('6-months-button', 'n_clicks'),
     Input('1-month-button', 'n_clicks'),
     Input('5-days-button', 'n_clicks'),
     Input('1-day-button', 'n_clicks'),
     Input('stock-graph', 'relayoutData')]
)
def update_graph(selected_stock, n_clicks_5y, n_clicks_1y, n_clicks_6m, n_clicks_1m, n_clicks_5d, n_clicks_1d, relayoutData):
    # Determine the selected time range based on the button clicks
    time_range = None
    if n_clicks_5y:
        time_range = '5y'
    elif n_clicks_1y:
        time_range = '1y'
    elif n_clicks_6m:
        time_range = '6m'
    elif n_clicks_1m:
        time_range = '1m'
    elif n_clicks_5d:
        time_range = '5d'
    elif n_clicks_1d:
        time_range = '1d'

    # Build the URL for the GET request to the backend
    backend_url = f"http://127.0.0.1:8080/stocks/datefrom/01.01.2020 01:01:01.000/dateto/28.09.2024 01:01:01.000/code/{selected_stock}"

    # Make a GET request to fetch stock data from the backend
    try:
        response = requests.get(backend_url)
        response.raise_for_status()  # Check if request was successful
        stock_data = response.json()

        print("API Response Data Length:", len(stock_data))
    except requests.exceptions.RequestException as e:
        return {}, f"Error fetching data: {str(e)}"

    # Check if stock_data is valid and has the necessary structure
    if not stock_data or not isinstance(stock_data, list):
        return {}, "No data available or invalid format"

    # Convert the stock data to a Pandas DataFrame
    df = pd.DataFrame(stock_data)

    # Ensure the 'local_time' column is in datetime format
    df['local_time'] = pd.to_datetime(df['local_time'])
    
    
    if relayoutData and 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
        start_time = pd.to_datetime(relayoutData['xaxis.range[0]']).tz_localize('UTC').tz_convert("Australia/Sydney")
        end_time = pd.to_datetime(relayoutData['xaxis.range[1]']).tz_localize('UTC').tz_convert("Australia/Sydney")
        df_filtered = df[(df['local_time'] >= start_time) & (df['local_time'] <= end_time)]
        
        # To avoid a SettingWithCopy warning when apply .iloc to the data frame
        df_filtered = df_filtered.copy()
    else:
    # If no zooming is done, use the full dataset
        df_filtered = df

    # Prepare the data for the graph
    stock_times = df_filtered['local_time']  # Using the DataFrame column
    stock_close_prices = df_filtered['close']  # Using the DataFrame column

    df_filtered['EMA'] = df_filtered['close'].ewm(span=10, adjust=False).mean()
    stock_ema = df_filtered['EMA']

    # Create the figure for the graph
    figure = {
        'data': [
            go.Scatter(
                x=stock_times,
                y=stock_close_prices,
                mode='markers',
                name=f'{selected_stock}',
                marker=dict(size=3)
            ),
            go.Scatter(
                x=stock_times,
                y=stock_ema,
                mode='markers',
                name=f'{selected_stock} EMA (10-day)',
                line=dict(color='orange'),
                marker=dict(size=2)
            )
        ],
        'layout': go.Layout(
            title=f"Stock: {selected_stock} ({time_range})",
            xaxis={'title': 'Time', 'showgrid': False},
            yaxis={'title': 'Close Price', 'showgrid': False},
        )
    }

    sma_total = 0

    for close in stock_close_prices:
        sma_total += close
    
    sma = sma_total / len(stock_close_prices);

    sma_info = f"SMA (Simple Moving Average): {round(sma, 3)}, calculated over {len(stock_close_prices)} points"

    period = len(df_filtered['close']) # Weighted moving average period equal to number of data points
    df_filtered['WMA'] = calculate_wma(df_filtered, period)
    wma = df_filtered['WMA'].iloc[-1]

    wma_info = f'The Weighted Moving Average for {len(df_filtered['close'])} points is {wma}'

    # Stock information (showing the last close price and time)
    last_entry = df_filtered.iloc[-1] if not df_filtered.empty else {}
    stock_code = last_entry.get('code', 'N/A')
    last_close_price = last_entry.get('close', 0)
    last_time = last_entry.get('local_time', 'N/A')
    info = f"Stock: {stock_code}, Last close price: {last_close_price}, Time: {last_time}"

    return figure, info, sma_info, wma_info

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
    
    # Use rolling to apply the WMA over the specified period
    wma = df['close'].rolling(window=period).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    
    return wma

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
