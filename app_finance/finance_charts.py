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

        # Filter data to last 24 hours (approx 96 15-min intervals)
        filtered_data = data.iloc[-96:].copy()

        chart_title = f"{symbol} (15m)"
        img_base64 = create_candlestick_chart_image(filtered_data, chart_title)
        charts[symbol] = img_base64

    # You can add logic here to generate charts with indicators (EMA, KRI, Quarter Theory)
    # For now, I'll generate basic candlestick charts as a starting point.
    # Adapting the indicator logic from the Streamlit code would go here,
    # calling create_candlestick_chart_image with the data and overlays.

    # Example for GBPJPY with indicators (adapt as needed)
    gbpjpy_data = get_financial_data("GBPJPY=X", period="1wk", interval="15m").iloc[-96:].copy()
    if not gbpjpy_data.empty:
        gbpjpy_data_ohlc = gbpjpy_data[['Open', 'High', 'Low', 'Close']].copy()
        gbpjpy_data_ohlc['Date'] = gbpjpy_data_ohlc.index.map(mpl_dates.date2num)
        ohlc_values = [tuple(x) for x in gbpjpy_data_ohlc[['Date', 'Open', 'High', 'Low', 'Close']].values]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_facecolor('black')
        candlestick_ohlc(ax, ohlc_values, width=0.0006, colorup='g', colordown='r')
        ax.set_title("GBPJPY (15m) with Indicators")
        ax.xaxis.set_major_formatter(mpl_dates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45, ha='right')

        # Quarter Theory levels
        last_price = gbpjpy_data['Close'].iloc[-1].item()
        nearest_quarter = round(last_price * 4) / 4
        upper_quarter = nearest_quarter + 0.250
        lower_quarter = nearest_quarter - 0.250
        ax.axhline(upper_quarter, color='green', linestyle='--')
        ax.text(x=gbpjpy_data_ohlc['Date'].iloc[-1], y=upper_quarter, s=str(round(upper_quarter, 3)), color='green')
        ax.axhline(lower_quarter, color='red', linestyle='--')
        ax.text(x=gbpjpy_data_ohlc['Date'].iloc[-1], y=lower_quarter, s=str(round(lower_quarter, 3)), color='red')

        # 50-period EMA
        ema_50 = get_financial_data("GBPJPY=X", period="1wk", interval="15m")['Close'].ewm(span=50).mean()
        ax.plot(gbpjpy_data_ohlc['Date'], ema_50.iloc[-96:], color='white', label='EMA 50')

        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        charts["GBPJPY=X_indicators"] = base64.b64encode(buf.read()).decode('utf-8')


    # Example for AUDJPY with indicators (adapt as needed)
    audjpy_data = get_financial_data("AUDJPY=X", period="1wk", interval="15m").iloc[-96:].copy()
    if not audjpy_data.empty:
        audjpy_data_ohlc = audjpy_data[['Open', 'High', 'Low', 'Close']].copy()
        audjpy_data_ohlc['Date'] = audjpy_data_ohlc.index.map(mpl_dates.date2num)
        ohlc_values = [tuple(x) for x in audjpy_data_ohlc[['Date', 'Open', 'High', 'Low', 'Close']].values]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_facecolor('black')
        candlestick_ohlc(ax, ohlc_values, width=0.0006, colorup='g', colordown='r')
        ax.set_title("AUDJPY (15m) with Indicators")
        ax.xaxis.set_major_formatter(mpl_dates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45, ha='right')

        # Quarter Theory levels
        last_price = audjpy_data['Close'].iloc[-1].item()
        nearest_quarter = round(last_price * 4) / 4
        upper_quarter = nearest_quarter + 0.250
        lower_quarter = nearest_quarter - 0.250
        ax.axhline(upper_quarter, color='green', linestyle='--')
        ax.text(x=audjpy_data_ohlc['Date'].iloc[-1], y=upper_quarter, s=str(round(upper_quarter, 3)), color='green')
        ax.axhline(lower_quarter, color='red', linestyle='--')
        ax.text(x=audjpy_data_ohlc['Date'].iloc[-1], y=lower_quarter, s=str(round(lower_quarter, 3)), color='red')

        # 50-period EMA
        ema_50 = get_financial_data("AUDJPY=X", period="1wk", interval="15m")['Close'].ewm(span=50).mean()
        ax.plot(audjpy_data_ohlc['Date'], ema_50.iloc[-96:], color='white', label='EMA 50')

        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        charts["AUDJPY=X_indicators"] = base64.b64encode(buf.read()).decode('utf-8')

    # Example for BTC-USD with indicators (adapt as needed)
    btcusd_data = get_financial_data("BTC-USD", period="1wk", interval="15m").iloc[-96:].copy()
    if not btcusd_data.empty:
        btcusd_data_ohlc = btcusd_data[['Open', 'High', 'Low', 'Close']].copy()
        btcusd_data_ohlc['Date'] = btcusd_data_ohlc.index.map(mpl_dates.date2num)
        ohlc_values = [tuple(x) for x in btcusd_data_ohlc[['Date', 'Open', 'High', 'Low', 'Close']].values]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_facecolor('black')
        candlestick_ohlc(ax, ohlc_values, width=0.0006, colorup='g', colordown='r')
        ax.set_title("BTC-USD (15m) with KRI")
        ax.xaxis.set_major_formatter(mpl_dates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45, ha='right')

        # Kairi Relative Index (KRI) with Arrows
        length = 14
        src = get_financial_data("BTC-USD", period="1wk", interval="15m")['Close']
        sma = src.rolling(window=length).mean()
        kri = 100 * (src - sma) / sma

        # Buy/Sell signals
        buySignal = pd.Series(False, index=btcusd_data.index)
        sellSignal = pd.Series(False, index=btcusd_data.index)
        for i in range(1, len(btcusd_data)):
            if kri.iloc[i-1].item() < 0 and kri.iloc[i].item() >= 0:
                buySignal.iloc[i] = True
            elif kri.iloc[i-1].item() > 0 and kri.iloc[i].item() <= 0:
                sellSignal.iloc[i] = True

        # Plot Buy/Sell signals
        ax.plot(btcusd_data_ohlc['Date'][buySignal.values], btcusd_data_ohlc['Low'][buySignal.values], '^', markersize=5, color='green', label='Buy Signal')
        ax.plot(btcusd_data_ohlc['Date'][sellSignal.values], btcusd_data_ohlc['High'][sellSignal.values], 'v', markersize=5, color='red', label='Sell Signal')


        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        charts["BTC-USD_indicators"] = base64.b64encode(buf.read()).decode('utf-8')


    return charts

# Example usage (for testing the module independently)
if __name__ == '__main__':
    generated_charts = generate_dashboard_charts()
    for symbol, img_data in generated_charts.items():
        if img_data:
            print(f"Generated chart for {symbol}: {len(img_data)} bytes (base64)")
        else:
            print(f"Failed to generate chart for {symbol}")