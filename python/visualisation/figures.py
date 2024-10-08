import plotly.graph_objects as go
from calculations.math_calcs import calculate_macd, calculate_true_range, calculate_dm, calculate_di
from calculations.math_calcs import calculate_adx, calculate_parabolic_sar, calculate_rsi, calculate_stochastic_oscillator
from calculations.math_calcs import calculate_cci, calculate_bollinger_bands, calculate_atr

def generate_figures(df_filtered, selected_graph_type, selected_stock, stock_times, stock_close_prices, time_range):
    asterix_info = ''
    
    uniform_x = list(range(len(df_filtered)))

    num_ticks = 3 if len(df_filtered) < 4 else 4  # Show 3 or 4 ticks depending on data size
    step = max(1, len(df_filtered) // num_ticks)  # Ensure dynamic spacing based on visible data
    reduced_x = uniform_x[::step]  # Uniform x values reduced
    reduced_dates = stock_times.dt.strftime('%d-%m-%Y')[::step]
    
    if (selected_graph_type == 'Standard / OHLC'):
        figure = {
            'data': [
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['open'],
                    mode='lines',
                    name=f'{selected_stock} open',
                    line=dict(color='blue'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                ),
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['high'],
                    mode='lines',
                    name=f'{selected_stock} high',
                    line=dict(color='darkgrey'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                ),
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['low'],
                    mode='lines',
                    name=f'{selected_stock} low',
                    line=dict(color='lightblue'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                ),
                go.Scatter(
                    x=uniform_x,
                    y=stock_close_prices,
                    mode='lines',
                    name=f'{selected_stock} close',
                    line=dict(color='red'),
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
                yaxis={'title': 'Price (USD)', 'showgrid': False},
            )
        }
    elif (selected_graph_type == 'EMA - Exponential Moving Average'):
        df_filtered['EMA'] = df_filtered['close'].ewm(span=10, adjust=False).mean()
        stock_ema = df_filtered['EMA']

        figure = {
            'data': [
                go.Scatter(
                    x=uniform_x,
                    y=stock_close_prices,
                    mode='lines',
                    name=f'{selected_stock} close',
                    line=dict(color='red'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                ),
                go.Scatter(
                    x=uniform_x,
                    y=stock_ema,
                    mode='lines',
                    name=f'{selected_stock} EMA (period: 10)',
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
                yaxis={'title': 'Price (USD)', 'showgrid': False},
            )
        }
    elif (selected_graph_type == 'MACD - Moving Average Convergence/Divergence'):
        df_macd = calculate_macd(df_filtered)

        asterix_info = 'Moving Average Convergence/Divergence shows the relationship between two EMAs. MACD = 12-period EMA - 26-period EMA'

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
                yaxis={'title': 'Diff', 'showgrid': False},
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
                yaxis={'title': 'Strength of Trend', 'showgrid': False},
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
                        marker=dict(size=3),
                        text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                        hoverinfo='text+y'
                    ),
                    go.Scatter(
                        x=uniform_x,
                        y=df_filtered['high'],
                        mode='lines',
                        name=f'{selected_stock} High',
                        line=dict(color='darkgrey'),
                        marker=dict(size=2),
                        text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                        hoverinfo='text+y'
                    ),
                    go.Scatter(
                        x=uniform_x,
                        y=df_filtered['low'],
                        mode='lines',
                        name=f'{selected_stock} Low',
                        line=dict(color='lightblue'),
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
                    yaxis={'title': 'Price (USD)', 'showgrid': False},
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
                yaxis={'title': 'Range', 'showgrid': False},
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
                yaxis={'title': 'Range', 'showgrid': False},
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
                yaxis={'title': 'CCI Range', 'showgrid': False},
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
                    line=dict(color='darkgrey'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                ),
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['Middle Band'],
                    mode='lines',
                    name=f'{selected_stock} Middle Band (period: 20)',
                    line=dict(color='orange'),
                    marker=dict(size=2),
                    text=stock_times.dt.strftime('%d-%m-%Y, %r'),
                    hoverinfo='text+y'
                ),
                go.Scatter(
                    x=uniform_x,
                    y=df_filtered['Lower Band'],
                    mode='lines',
                    name=f'{selected_stock} Lower Band (period: 20)',
                    line=dict(color='lightblue'),
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
                yaxis={'title': 'Price (USD)', 'showgrid': False},
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
                yaxis={'title': 'ATR Value', 'showgrid': False},
            )
        }
    return asterix_info, figure