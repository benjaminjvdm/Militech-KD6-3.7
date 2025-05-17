from pyharmonics.marketdata import YahooCandleData
b = YahooCandleData()
b.get_candles('GBPJPY=X', b.MIN_5, 1000)
b.df
print(b.df)


