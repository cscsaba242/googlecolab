class MException(Exception):
    def __init__(self, message, symbol=None, broker=None):
        message = f"[{broker}] [{symbol}] {message}"
        super().__init__(message)
        self.symbol = symbol
        self.broker = broker