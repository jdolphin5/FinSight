from flask import Flask, jsonify
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import requests
import pandas as pd  # Import pandas for data manipulation
from math_calcs import calculate_wma, calculate_macd, calculate_true_range, calculate_dm, calculate_di
from math_calcs import calculate_adx, calculate_parabolic_sar, calculate_rsi, calculate_stochastic_oscillator
from math_calcs import calculate_cci, calculate_bollinger_bands, calculate_atr

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
available_graph_types = ['Standard', 'MACD - Moving Average Convergence/Divergence', 'ADX - Average Directional Index', 'Parabolic SAR - Stop and Reverse',
                         'RSI - Relative Strength Index', '%K - Stochastic Oscillator', 'CCI - Commodity Channel Index',
                         'Bollinger Bands', 'ATR - Average True Range']

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

    dcc.Dropdown(
        id='graph-type-dropdown',
        options=[{'label': graph_type, 'value': graph_type} for graph_type in available_graph_types],
        value='Standard',
        placeholder='Select Graph Type'
    ),

    # Buttons for time range selection
    html.Div([
        html.Button('5 Years', id='5-years-button', n_clicks=0, style={'background-color': colours['button-bg1'], 'color': colours['button-text1']}),
        html.Button('1 Year', id='1-year-button', n_clicks=0, style={'background-color': colours['button-bg1'], 'color': colours['button-text1']}),
        html.Button('6 Months', id='6-months-button', n_clicks=0, style={'background-color': colours['button-bg1'], 'color': colours['button-text1']}),
        html.Button('1 Month', id='1-month-button', n_clicks=0, style={'background-color': colours['button-bg1'], 'color': colours['button-text1']}),
        html.Button('5 Days', id='5-days-button', n_clicks=0, style={'background-color': colours['button-bg1'], 'color': colours['button-text1']}),
        html.Button('1 Day', id='1-day-button', n_clicks=0, style={'background-color': colours['button-bg1'], 'color': colours['button-text1']}),
    ], style={'display': 'flex', 'gap': '10px', 'margin': '10px 0'}),

    dcc.Graph(id='stock-graph'),
    html.Br(),
    html.Div(id='asterix-info'),
    html.Div(id='stock-info'),
    html.Div(id='simple-moving-average'),
    html.Div(id='weighted-moving-average')
], style={'color': colours['text'], 'background-color': colours['background'], 'font-family': 'Arial'})

@app.callback(
    [Output('stock-graph', 'figure'), Output('asterix-info', 'children'), Output('stock-info', 'children'), Output('simple-moving-average', 'children'), Output('weighted-moving-average', 'children')],
    [Input('stock-dropdown', 'value'),
     Input('graph-type-dropdown', 'value'),
     Input('5-years-button', 'n_clicks'),
     Input('1-year-button', 'n_clicks'),
     Input('6-months-button', 'n_clicks'),
     Input('1-month-button', 'n_clicks'),
     Input('5-days-button', 'n_clicks'),
     Input('1-day-button', 'n_clicks'),
     Input('stock-graph', 'relayoutData')]
)
def update_graph(selected_stock, selected_graph_type, n_clicks_5y, n_clicks_1y, n_clicks_6m, n_clicks_1m, n_clicks_5d, n_clicks_1d, relayoutData):
    # Determine the selected time range based on the button clicks
    time_range = 'Default'
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

    uniform_x = list(range(len(df_filtered)))

    num_ticks = 3 if len(df_filtered) < 4 else 4  # Show 3 or 4 ticks depending on data size
    step = max(1, len(df_filtered) // num_ticks)  # Ensure dynamic spacing based on visible data
    reduced_x = uniform_x[::step]  # Uniform x values reduced
    reduced_dates = stock_times.dt.strftime('%d-%m-%Y')[::step]

    df_filtered['EMA'] = df_filtered['close'].ewm(span=10, adjust=False).mean()
    stock_ema = df_filtered['EMA']

    asterix_info = ''

    figure = {
        'data': [
            go.Scatter(
                x=uniform_x,
                y=stock_close_prices,
                mode='lines',
                name=f'{selected_stock}',
                marker=dict(size=3),
                text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                hoverinfo='text+y'
            ),
            go.Scatter(
                x=uniform_x,
                y=stock_ema,
                mode='lines',
                name=f'{selected_stock} EMA (10-day)',
                line=dict(color='orange'),
                marker=dict(size=2),
                text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                hoverinfo='text+y'
            )
        ],
        'layout': go.Layout(
            title=f"Stock: {selected_stock} ({time_range})",
            xaxis_title="Date",
            xaxis=dict(
                tickmode='array',
                tickvals=reduced_x,  # Positions of ticks are reduced uniform x-values
                ticktext=reduced_dates  # Show reduced set of actual dates at each tick
            ),
            yaxis={'title': 'Price', 'showgrid': False},
        )
    }

    # Create the figure for the graph
    if (selected_graph_type == 'Standard'):
        figure = {
            'data': [
                go.Scatter(
                    x=uniform_x,
                    y=stock_close_prices,
                    mode='lines',
                    name=f'{selected_stock}',
                    marker=dict(size=3),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                ),
                go.Scatter(
                    x=uniform_x,
                    y=stock_ema,
                    mode='lines',
                    name=f'{selected_stock} EMA (10-day)',
                    line=dict(color='orange'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                )
            ],
            'layout': go.Layout(
                title=f"Stock: {selected_stock} ({time_range})",
                xaxis_title="Date",
                xaxis=dict(
                    tickmode='array',
                    tickvals=reduced_x,  # Positions of ticks are reduced uniform x-values
                    ticktext=reduced_dates  # Show reduced set of actual dates at each tick
                ),
                yaxis={'title': 'Price', 'showgrid': False},
            )
        }
    elif (selected_graph_type == 'MACD - Moving Average Convergence/Divergence'):
        df_macd = calculate_macd(df_filtered)

        asterix_info = 'Moving Average Convergence/Divergence shows the relationship between two EMAs.'

        figure = {
            'data': [
                go.Scatter(
                    x=uniform_x,
                    y=df_macd['MACD'],
                    mode='lines',
                    name=f'{selected_stock} MACD',
                    line=dict(color='orange'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                ),
                go.Scatter(
                    x=uniform_x,
                    y=df_macd['Signal_Line'],
                    mode='lines',
                    name='Signal Line',
                    line=dict(color='green'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                )
            ],
            'layout': go.Layout(
                title=f"Stock: {selected_stock} ({time_range})",
                xaxis_title="Date",
                xaxis=dict(
                    tickmode='array',
                    tickvals=reduced_x,  # Positions of ticks are reduced uniform x-values
                    ticktext=reduced_dates  # Show reduced set of actual dates at each tick
                ),
                yaxis={'title': 'Price', 'showgrid': False},
            )
        }
    elif (selected_graph_type == 'ADX - Average Directional Index'):        
        df_filtered = calculate_true_range(df_filtered)
        df_filtered = calculate_dm(df_filtered)
        df_filtered = calculate_di(df_filtered, period=14)
        df_filtered = calculate_adx(df_filtered, period=14)

        asterix_info = "Average Directional Index measures the strength of a trend regardless of its direction"

        figure = {
            'data': [
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['ADX'],
                    mode='lines',
                    name=f'{selected_stock} ADX (period: 14)',
                    line=dict(color='orange'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                )
            ],
            'layout': go.Layout(
                title=f"Stock: {selected_stock} ({time_range})",
                xaxis_title="Date",
                xaxis=dict(
                    tickmode='array',
                    tickvals=reduced_x,  # Positions of ticks are reduced uniform x-values
                    ticktext=reduced_dates  # Show reduced set of actual dates at each tick
                ),
                yaxis={'title': 'Price', 'showgrid': False},
            )
        }
    elif (selected_graph_type == 'Parabolic SAR - Stop and Reverse'):
        if (len(df_filtered) == 0):
            asterix_info = 'There is no data in this range'

        else:
            df_filtered = calculate_parabolic_sar(df_filtered)

            asterix_info = "Parabolic Stop and Reverse is a time/price-based indicator used to identify potential reverse points. *AF = Acceleration Factor, initial_af=0.02, max_af=0.20, step_af=0.02"

            figure = {
                'data': [
                    go.Scatter(
                        x=uniform_x,
                        y=df_filtered['SAR'],
                        mode='lines',
                        name=f'{selected_stock} SAR',
                        line=dict(color='orange'),
                        marker=dict(size=4),
                        text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                        hoverinfo='text+y'
                    ),
                                    go.Scatter(
                        x=uniform_x,
                        y=df_filtered['high'],
                        mode='lines',
                        name=f'{selected_stock} High',
                        line=dict(color='red'),
                        marker=dict(size=2),
                        text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                        hoverinfo='text+y'
                    ),
                    go.Scatter(
                        x=uniform_x,
                        y=df_filtered['low'],
                        mode='lines',
                        name=f'{selected_stock} Low',
                        line=dict(color='blue'),
                        marker=dict(size=2),
                        text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                        hoverinfo='text+y'
                    )
                ],
                'layout': go.Layout(
                    title=f"Stock: {selected_stock} ({time_range})",
                    xaxis_title="Date",
                    xaxis=dict(
                        tickmode='array',
                        tickvals=reduced_x,  # Positions of ticks are reduced uniform x-values
                        ticktext=reduced_dates  # Show reduced set of actual dates at each tick
                    ),
                    yaxis={'title': 'Price', 'showgrid': False},
                )
            }
    elif (selected_graph_type == 'RSI - Relative Strength Index'):
        df_filtered = calculate_rsi(df_filtered)

        asterix_info = 'Relative Strength Index measures the speed and change of price movements.'

        figure = {
            'data': [
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['RSI'],
                    mode='lines',
                    name=f'{selected_stock} RSI (period: 14)',
                    line=dict(color='orange'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                )
            ],
            'layout': go.Layout(
                title=f"Stock: {selected_stock} ({time_range})",
                xaxis_title="Date",
                xaxis=dict(
                    tickmode='array',
                    tickvals=reduced_x,  # Positions of ticks are reduced uniform x-values
                    ticktext=reduced_dates  # Show reduced set of actual dates at each tick
                ),
                yaxis={'title': 'RSI', 'showgrid': False},
            )
        }

    elif (selected_graph_type == '%K - Stochastic Oscillator'):  
        df_filtered = calculate_stochastic_oscillator(df_filtered)

        asterix_info = 'Stochastic Oscillator compares a particular closing price to a range of prices over a certain period. Period=14'

        figure = {
            'data': [
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['stochastic_k'],
                    mode='lines',
                    name=f'{selected_stock} Stochastic Oscillator (period: 14)',
                    line=dict(color='orange'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                )
            ],
            'layout': go.Layout(
                title=f"Stock: {selected_stock} ({time_range})",
                xaxis_title="Date",
                xaxis=dict(
                    tickmode='array',
                    tickvals=reduced_x,  # Positions of ticks are reduced uniform x-values
                    ticktext=reduced_dates  # Show reduced set of actual dates at each tick
                ),
                yaxis={'title': 'Stochastic K', 'showgrid': False},
            )
        }

    elif (selected_graph_type == 'CCI - Commodity Channel Index'):  
        df_filtered = calculate_cci(df_filtered)

        asterix_info = 'Commodity Channel Index measures the variation of a security\'s price from it\'s statistical mean.'

        figure = {
            'data': [
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['CCI'],
                    mode='lines',
                    name=f'{selected_stock} Commodity Channel Index (period: 20)',
                    line=dict(color='orange'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                )
            ],
            'layout': go.Layout(
                title=f"Stock: {selected_stock} ({time_range})",
                xaxis_title="Date",
                xaxis=dict(
                    tickmode='array',
                    tickvals=reduced_x,  # Positions of ticks are reduced uniform x-values
                    ticktext=reduced_dates  # Show reduced set of actual dates at each tick
                ),
                yaxis={'title': 'CCI', 'showgrid': False},
            )
        }

    elif (selected_graph_type == 'Bollinger Bands'):  
        df_filtered = calculate_bollinger_bands(df_filtered)

        asterix_info = 'Bollinger Bands consist of a middle SMA band and two outer bands based on standard deviations.'

        figure = {
            'data': [
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['Upper Band'],
                    mode='lines',
                    name=f'{selected_stock} Upper Band (period: 20)',
                    line=dict(color='orange'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                ),
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['Middle Band'],
                    mode='lines',
                    name=f'{selected_stock} Middle Band (period: 20)',
                    line=dict(color='green'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                ),
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['Lower Band'],
                    mode='lines',
                    name=f'{selected_stock} Lower Band (period: 20)',
                    line=dict(color='blue'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                )
            ],
            'layout': go.Layout(
                title=f"Stock: {selected_stock} ({time_range})",
                xaxis_title="Date",
                xaxis=dict(
                    tickmode='array',
                    tickvals=reduced_x,  # Positions of ticks are reduced uniform x-values
                    ticktext=reduced_dates  # Show reduced set of actual dates at each tick
                ),
                yaxis={'title': 'Bollinger Bands', 'showgrid': False},
            )
        }

    elif (selected_graph_type == 'ATR - Average True Range'):  
        df_filtered = calculate_atr(df_filtered)

        asterix_info = 'Measures market volatility by decomposing the entire range of an asset price for that period.'

        figure = {
            'data': [
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['ATR'],
                    mode='lines',
                    name=f'{selected_stock} Average True Range (period: 14)',
                    line=dict(color='orange'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                )
            ],
            'layout': go.Layout(
                title=f"Stock: {selected_stock} ({time_range})",
                xaxis_title="Date",
                xaxis=dict(
                    tickmode='array',
                    tickvals=reduced_x,  # Positions of ticks are reduced uniform x-values
                    ticktext=reduced_dates  # Show reduced set of actual dates at each tick
                ),
                yaxis={'title': 'ATR', 'showgrid': False},
            )
        }

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
