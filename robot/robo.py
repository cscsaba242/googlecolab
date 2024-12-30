import requests
from datetime import datetime, timedelta
import time
import os
import json
import pandas
import pandas_ta as ta
from backtesting import Strategy, Backtest
import telegram as tg
import smacross
import asyncio

#class Main():
#  COLS=['Date','Open','High','Low','Close']
#  DF=pandas.DataFrame()
#  comp=100
#  logger=None
#  strategy=None
#  MAX_CANDLES = 200
#  PERIOD_LENGTH_SEC=5 #period in sec
#  PERIODS=200  # periods in PERIOD
#  PERIOD_GROUP=20 #period to send message
#  #DATA_STRUCT_CATEGORY = "linear"
#  SYMBOL = "BTCUSDT"
#
#  def __init__(self, logger, strategy, ):
#    self.strategy = strategy
#    self.logger
#
#  def convNum(self, dfParam: pandas.Series):
#    return (pandas.to_numeric(dfParam)*100).astype(int)
#
#
#  def getPrices(self, categoryParam, symbolParam, limitParam) -> pandas.DataFrame:
#    global SY
#    lf=pandas.DataFrame()
#    url = f"https://api-testnet.bybit.com/v5/market/mark-price-kline?category={categoryParam}&symbol={symbolParam}&interval=1&limit={limitParam}"
#    resp=requests.request("GET", url, headers=self.headers, data=self.payload).json()
#
#    lf = pandas.DataFrame(resp["result"]["list"], columns=self.COLS)
#    lf['Date'] = pandas.to_datetime(lf['Date'].astype(float))
#    lf['Open'] = self.convNum(lf['Open'])
#    lf['High'] = self.convNum(lf['High'])
#    lf['Low'] = self.convNum(lf['Low'])
#    lf['Close'] = self.convNum(lf['Close'])
#
#    self.logger.info(f"{lf.size=}, {resp['retCode']=}, {resp['retMsg']=}")
#    return lf
#
#  def main(self):
#    limit = self.MAX_CANDLES if DF.empty else 1
#    lf = self.getPrices("linear", self.SYMBOL, limit)
#
#    if DF.empty:
#      DF=lf.copy()
#    else:
#      DF = pandas.concat([lf,DF], ignore_index=True)
#
#  async def loop(self):
#    PERIOD=0
#    global logger
#    global DF
#    global CHAT_ID
#    global PERIOD_LENGTH_SEC
#    global PERIODS
#    global PERIOD_GROUP
#    global COMP
#
#    while PERIOD < PERIODS:
#      logger.info(f"\n{PERIOD=}")
#      self.main()
#      logger.info(f"{DF.size=}")
#      backtest = Backtest(DF, SmaCross,cash=10000 * COMP, commission=.002,exclusive_orders=True)
#      backtestOptimized=backtest.optimize(sma_f=[5, 10, 15], sma_s=[10, 20, 40], constraint=lambda p: p.sma_f < p.sma_s)
#      optStrategy = backtestOptimized._strategy
#      logger.info(f"{optStrategy.equity=}, {optStrategy.orders=}, {optStrategy.position=}, {optStrategy.trades=}")
#      logger.info(f"{optStrategy.sma_f=}, {optStrategy.sma_s=}")
#      backtest.sma_f = optStrategy.sma_f
#      backtest.sma_s = optStrategy.sma_s
#
#      if (PERIOD % PERIOD_GROUP) == 0:
#        await send_telegram_doc()
#      
#      time.sleep(PERIOD_LENGTH_SEC)
#      PERIOD += 1
#
#logger.info(f"{SYMBOL=}, {PERIOD_LENGTH_SEC=}, {PERIODS=}, {PERIOD_GROUP=}, {DATA_STRUCT_CATEGORY=}")
#asyncio.run(loop())

