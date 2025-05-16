import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from mplfinance.original_flavor import candlestick_ohlc
import base64
from io import BytesIO

def get_financial_data(symbol, period="1wk", interval="15m"):
    """Fetches financial data for a given symbol."""
    data = yf.download(symbol, period=period, interval=interval)
    return data

def create_candlestick_chart_image(data, title):
    """Creates a candlestick chart and returns it as a base64 encoded PNG image."""
    if data.empty:
        return None # Return None if no data is available

    # Ensure data is in the correct format for candlestick_ohlc
    data_ohlc = data[['Open', 'High', 'Low', 'Close']].copy()
    data_ohlc['Date'] = data_ohlc.index.map(mpl_dates.date2num)
    ohlc_values = [tuple(x) for x in data_ohlc[['Date', 'Open', 'High', 'Low', 'Close']].values]

    fig, ax = plt.subplots(figsize=(10, 6)) # Adjust figure size as needed
    ax.set_facecolor('black')

    candlestick_ohlc(ax, ohlc_values, width=0.0006, colorup='g', colordown='r')

    ax.set_title(title)
    ax.xaxis.set_major_formatter(mpl_dates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45, ha='right') # Rotate date labels

    # Save the chart to a BytesIO object
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig) # Close the figure to free up memory
    buf.seek(0)

    # Encode the image as base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

def generate_dashboard_charts():
    """Generates all charts for the dashboard."""
    charts = {}
    symbols = ["GBPJPY=X", "AUDJPY=X", "BTC-USD"]

    for symbol in symbols:
        data = get_financial_data(symbol, period="1wk", interval="15m")

        # Filter data to last 50 candles
        filtered_data = data.iloc[-30:].copy()

        chart_title = f"{symbol} (15m)"
        img_base64 = create_candlestick_chart_image(filtered_data, chart_title)
        charts[symbol] = img_base64

    return charts

# Example usage (for testing the module independently)
if __name__ == '__main__':
    generated_charts = generate_dashboard_charts()
    for symbol, img_data in generated_charts.items():
        if img_data:
            print(f"Generated chart for {symbol}: {len(img_data)} bytes (base64)")
        else:
            print(f"Failed to generate chart for {symbol}")