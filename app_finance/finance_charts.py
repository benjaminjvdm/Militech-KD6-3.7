from pyharmonics.marketdata import YahooCandleData
from pyharmonics.technicals import OHLCTechnicals
from pyharmonics.search import HarmonicSearch
from pyharmonics.plotter import Plotter

b = YahooCandleData()
b.get_candles('GBPJPY=X', b.MIN_5, 1000)
b.df
print(b.df)


t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=15)
t.df
print(t.df)

h = HarmonicSearch(t)

h.search()

patterns = h.get_patterns()


p = Plotter(t, 'GBPJPY=X', b.MIN_5)
p.add_harmonic_plots(h.get_patterns(family=h.XABCD)(formed=False))
p.show()