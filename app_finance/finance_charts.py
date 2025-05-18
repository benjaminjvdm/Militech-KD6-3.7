import time
from pyharmonics.marketdata import YahooCandleData
from pyharmonics.technicals import OHLCTechnicals
from pyharmonics.search import HarmonicSearch
from pyharmonics.plotter import Plotter
import plotly.graph_objects as go

def generate_dashboard_chart(symbol='GBPJPY=X', max_retries=5, delay_seconds=2):
    """
    Generates a Plotly figure for the given symbol, retrying data fetch if necessary.
    """
    b = YahooCandleData()
    
    for attempt in range(max_retries):
        b.get_candles(symbol, b.MIN_5, 1000)
        if not b.df.empty:
            print(f"Data fetched successfully for {symbol} on attempt {attempt + 1}")
            break
        else:
            print(f"Attempt {attempt + 1} failed to fetch data for {symbol}. Retrying in {delay_seconds} seconds...")
            time.sleep(delay_seconds)
            
    if b.df.empty:
        print(f"Failed to fetch data for {symbol} after {max_retries} attempts.")
        return go.Figure().to_image(format="png") # Return an empty figure image if no data after retries

    t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=3)
    h = HarmonicSearch(t)
    h.search()
    patterns = h.get_patterns()

    p = Plotter(t, plot_ema=False, plot_sma=False)
    p.add_harmonic_plots(h.get_patterns(family=h.XABCD))

    return p.to_image()
def generate_15min_chart(symbol='GBPJPY=X', max_retries=5, delay_seconds=2):
    """
    Generates a Plotly figure for the given symbol on a 15-minute timeframe, retrying data fetch if necessary.
    """
    b = YahooCandleData()
    
    for attempt in range(max_retries):
        b.get_candles(symbol, b.MIN_15, 1000)
        if not b.df.empty:
            print(f"Data fetched successfully for {symbol} on attempt {attempt + 1}")
            break
        else:
            print(f"Attempt {attempt + 1} failed to fetch data for {symbol}. Retrying in {delay_seconds} seconds...")
            time.sleep(delay_seconds)
            
    if b.df.empty:
        print(f"Failed to fetch data for {symbol} after {max_retries} attempts.")
        return go.Figure().to_image(format="png") # Return an empty figure image if no data after retries

    t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=3)
    h = HarmonicSearch(t)
    h.search()
    patterns = h.get_patterns()

    p = Plotter(t, plot_ema=False, plot_sma=False)
    p.add_harmonic_plots(h.get_patterns(family=h.XABCD))

    return p.to_image()
def generate_1hour_chart(symbol='GBPJPY=X', max_retries=5, delay_seconds=2):
    """
    Generates a Plotly figure for the given symbol on a 1-hour timeframe, retrying data fetch if necessary.
    """
    b = YahooCandleData()
    
    for attempt in range(max_retries):
        b.get_candles(symbol, b.HOUR_1, 1000)
        if not b.df.empty:
            print(f"Data fetched successfully for {symbol} on attempt {attempt + 1}")
            break
        else:
            print(f"Attempt {attempt + 1} failed to fetch data for {symbol}. Retrying in {delay_seconds} seconds...")
            time.sleep(delay_seconds)
            
    if b.df.empty:
        print(f"Failed to fetch data for {symbol} after {max_retries} attempts.")
        return go.Figure().to_image(format="png") # Return an empty figure image if no data after retries

    t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=3)
    h = HarmonicSearch(t)
    h.search()
    patterns = h.get_patterns()

    p = Plotter(t, plot_ema=False, plot_sma=False)
    p.add_harmonic_plots(h.get_patterns(family=h.XABCD))

    return p.to_image()