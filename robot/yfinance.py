
class YFinance():
    def __init__(self):
        pass

    def load_data(self, symbol, start, end, interval):
        import yfinance as yf
        data = yf.download(tickers=symbol, start=start, end=end, interval=interval)
        return data