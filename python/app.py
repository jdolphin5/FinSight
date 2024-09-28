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
    html.Div(id='stock-info')
])

@app.callback(
    [Output('stock-graph', 'figure'), Output('stock-info', 'children')],
    [Input('stock-dropdown', 'value'),
     Input('5-years-button', 'n_clicks'),
     Input('1-year-button', 'n_clicks'),
     Input('6-months-button', 'n_clicks'),
     Input('1-month-button', 'n_clicks'),
     Input('5-days-button', 'n_clicks'),
     Input('1-day-button', 'n_clicks')]
)
def update_graph(selected_stock, n_clicks_5y, n_clicks_1y, n_clicks_6m, n_clicks_1m, n_clicks_5d, n_clicks_1d):
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
    except requests.exceptions.RequestException as e:
        return {}, f"Error fetching data: {str(e)}"

    # Check if stock_data is valid and has the necessary structure
    if not stock_data or not isinstance(stock_data, list):
        return {}, "No data available or invalid format"

    # Convert the stock data to a Pandas DataFrame
    df = pd.DataFrame(stock_data)

    # Ensure the 'local_time' column is in datetime format
    df['local_time'] = pd.to_datetime(df['local_time'])

    # Prepare the data for the graph
    stock_times = df['local_time']  # Using the DataFrame column
    stock_close_prices = df['close']  # Using the DataFrame column


    # Create the figure for the graph
    figure = {
        'data': [go.Scatter(
            x=stock_times,
            y=stock_close_prices,
            mode='markers',
            name=f'{selected_stock}'
        )],
        'layout': go.Layout(
            title=f"Stock: {selected_stock} ({time_range})",
            xaxis={'title': 'Time', 'showgrid': False},
            yaxis={'title': 'Close Price', 'showgrid': False},
        )
    }

    # Stock information (showing the last close price and time)
    last_entry = df.iloc[-1] if not df.empty else {}
    stock_code = last_entry.get('code', 'N/A')
    last_close_price = last_entry.get('close', 0)
    last_time = last_entry.get('local_time', 'N/A')
    info = f"Stock: {stock_code}, Last close price: {last_close_price}, Time: {last_time}"

    return figure, info


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
