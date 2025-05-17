from pyharmonics.marketdata import YahooCandleData
from pyharmonics.technicals import OHLCTechnicals

b = YahooCandleData()
b.get_candles('GBPJPY=X', b.MIN_5, 100)
b.df
print(b.df)


t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=20)
t.df
print(t.df)