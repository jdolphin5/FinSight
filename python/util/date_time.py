from datetime import timedelta

def compute_time_frame(time_frame, now):

    # Set date format as "dd.MM.yyyy HH:mm:ss.SSS"
    date_format = "%d.%m.%Y %H:%M:%S.%f"

    # Calculate the start date based on the time frame
    if time_frame == 'Default':  # Default is 20 years
        start_date = now - timedelta(days=20 * 365)
    elif time_frame == '5y':
        start_date = now - timedelta(days=5 * 365)
    elif time_frame == '1y':
        start_date = now - timedelta(days=365)
    elif time_frame == '6m':
        start_date = now - timedelta(days=6 * 30)  # Approximation for months
    elif time_frame == '1m':
        start_date = now - timedelta(days=30)  # Approximation for months
    elif time_frame == '5d':
        start_date = now - timedelta(days=5)
    elif time_frame == '1d':
        start_date = now - timedelta(days=1)
    else:
        raise ValueError("Invalid time frame. Choose from 'Default', '5y', '1y', '6m', '1m', '5d', '1d'.")

    # Format start and end date to the requested format
    start_date_str = start_date.strftime(date_format)[:-3]  # Removing the last 3 digits to match SSS precision
    end_date_str = now.strftime(date_format)[:-3]  # Removing the last 3 digits to match SSS precision

    return start_date_str, end_date_str