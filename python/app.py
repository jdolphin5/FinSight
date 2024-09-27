# app.py
from flask import Flask, request, jsonify
from dash import Dash, html, dcc, Input, Output, callback
import plotly.graph_objs as go

# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app with Flask server
app = Dash(__name__, server=server)

# Global variable to store stock data
stock_data = {}

# Define Dash layout
app.layout = html.Div([
    html.H1("Stock Data Visualization"),
    dcc.Input(id='stock-code-input', type='text', value='AAPL', placeholder='Enter Stock Code'),
    html.Button('Update Graph', id='update-button', n_clicks=0),
    dcc.Graph(id='stock-graph'),
    html.Div(id='stock-info')
])

@app.callback(
    [Output('stock-graph', 'figure'), Output('stock-info', 'children')],
    [Input('stock-info', 'children')]
)
def update_graph(_):
    global stock_data

    # Check if stock_data is not empty and is a list
    if not stock_data or not isinstance(stock_data, list):
        return {}, "No data available or invalid format"

    # Extract data from the entire stock_data list
    times = [entry.get('local_time', 'N/A') for entry in stock_data]
    close_prices = [entry.get('close', 0) for entry in stock_data]
    stock_code = stock_data[0].get('code', 'N/A')  # Assuming all entries have the same stock code

    # Create the graph with all data points
    figure = {
        'data': [{
            'x': times,  # List of time points
            'y': close_prices,  # List of stock close prices
            'type': 'line',
            'name': stock_code
        }],
        'layout': {
            'title': f"Stock: {stock_code} Price Over Time",
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Close Price'}
        }
    }

    # Display stock information (you can customize this to display more details)
    info = f"Stock: {stock_code}, Number of data points: {len(stock_data)}"

    return figure, info



# Define endpoint to receive POST request from Spring Boot
@server.route('/update-stock', methods=['POST'])
def update_stock():
    global stock_data
    data = request.get_json()

    if not isinstance(data, list) or not data:
        return jsonify({"status": "failure", "reason": "Invalid data format"}), 400

    # Process each stock entry in the list
    stock_data = data  # Assuming you're overriding global stock_data with the new data

    return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
