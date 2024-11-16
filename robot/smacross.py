from backtesting import Strategy, Backtest
from backtesting.lib import crossover
from backtesting.test import SMA

class SmaCross(Strategy):
  global logger
  sma_f = 10
  sma_s = 20
  sma_f_func = None
  sma_s_func = None

  def __init__(self, logger):
    logger.info(f"SmaCross {self.sma_f,=}, {self.sma_s=}")

  def init(self):
    close = self.data.Close
    self.sma_f_func = self.I(SMA, close, self.sma_f)
    self.sma_s_func = self.I(SMA, close, self.sma_s)

  def next(self):
    if crossover(self.sma_f_func, self.sma_s_func):
      self.buy()
    elif crossover(self.sma_s_func, self.sma_f_func):
      self.sell()
