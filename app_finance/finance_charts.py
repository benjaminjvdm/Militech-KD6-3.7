from pyharmonics.marketdata import YahooCandleData
b = YahooCandleData()
b.get_candles('GBPJPY=X', b.MIN_5, 100)
b.df
b.df