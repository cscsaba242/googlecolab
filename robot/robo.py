import requests
from datetime import datetime, timedelta
import time
import os
import json
import pandas
import pandas_ta as ta
from backtesting import Strategy, Backtest
import telegram as tg
import asyncio

#Start,End,Duration,Exposure Time [%],Equity Final [$],Equity Peak [$],Return [%],
#Buy & Hold Return [%],Return (Ann.) [%],Volatility (Ann.) [%],Sharpe Ratio,Sortino Ratio
#Calmar Ratio,Max. Drawdown [%],Avg. Drawdown [%],Max. Drawdown Duration,Avg. Drawdown Duration,# Trades
#Win Rate [%],Best Trade [%],Worst Trade [%],Avg. Trade [%],Max. Trade Duration,Avg. Trade Duration
#Profit Factor,Expectancy [%],SQN,_strategy,_equity_curve,_trades

# 10,05 16:23 1728145380000 18:23 1728152580000
# 10,05 20:22 o:61920.30 h:61961.80 l:61920.30
# start = datetime.strptime("2024 10 05, 16:23:00", "%Y %m %d, %H:%M:%S").timestamp()
# start = int(round(start * 1000))
#getUpdates response:
#{'ok': True, 'result': [{'update_id': 3987255, 'message': {'message_id': 2, 'from':
#{'id': 5833186787, 'is_bot': False, 'first_name': 'bunnypussylover', 'username': 'bunnypussylover', 'language_code': 'en'},
#'chat': {'id': 5833186787, 'first_name': 'bunnypussylover', 'username': 'bunnypussylover', 'type': 'private'}, 'date': 1728931474, 'text': 'hi'}}]}
DOC_FILE="./robo.log"
IMG_FILE="./image.jpg"
BYBIT_MAX_CANDLES = 200
PERIOD_LENGTH_SEC=5 #period in sec
PERIODS=200  # periods in PERIOD
PERIOD_GROUP=20 #period to send message
DATA_STRUCT_CATEGORY = "linear"
SYMBOL = "BTCUSDT"


class Main():
  payload={};
  headers = {'User-Agent': 'Mozilla/5.0'}
  COLS=['Date','Open','High','Low','Close']
  DF=pandas.DataFrame()
  comp=100
  logger=None
  SmaCross=None

  def __init__(self, logger, strategy):
    self.SmaCross
    self.logger

  def convNum(self, dfParam: pandas.Series):
    return (pandas.to_numeric(dfParam)*100).astype(int)


  def getPrices(self, categoryParam, symbolParam, limitParam):
    global logger
    global headers
    global payload
    global COLS
    lf=pandas.DataFrame()
    url = f"https://api-testnet.bybit.com/v5/market/mark-price-kline?category={categoryParam}&symbol={symbolParam}&interval=1&limit={limitParam}"
    resp=requests.request("GET", url, headers=headers, data=payload).json()

    lf = pandas.DataFrame(resp["result"]["list"], columns=COLS)
    lf['Date'] = pandas.to_datetime(lf['Date'].astype(float))
    lf['Open'] = self.convNum(lf['Open'])
    lf['High'] = self.convNum(lf['High'])
    lf['Low'] = self.convNum(lf['Low'])
    lf['Close'] = self.convNum(lf['Close'])

    logger.info(f"{lf.size=}, {resp['retCode']=}, {resp['retMsg']=}")
    return lf

  def main(self):
    global DF
    global PERIOD_GROUP
    global logger
    global BYBIT_MAX_CANDLES
    global DATA_STRUCT_CATEGORY
    global SYMBOL

    limit = BYBIT_MAX_CANDLES if DF.empty else 1
    lf = self.getPrices(DATA_STRUCT_CATEGORY, SYMBOL, limit)

    if DF.empty:
      DF=lf.copy()
    else:
      DF = pandas.concat([lf,DF], ignore_index=True)

  async def loop(self):
    PERIOD=0
    global logger
    global DF
    global CHAT_ID
    global PERIOD_LENGTH_SEC
    global PERIODS
    global PERIOD_GROUP

    while PERIOD < PERIODS:
      logger.info(f"\n{PERIOD=}")
      self.main()
      logger.info(f"{DF.size=}")
      backtest = Backtest(DF, SmaCross,cash=10000*comp, commission=.002,exclusive_orders=True)
      backtestOptimized=backtest.optimize(sma_f=[5, 10, 15], sma_s=[10, 20, 40], constraint=lambda p: p.sma_f < p.sma_s)
      optStrategy = backtestOptimized._strategy
      logger.info(f"{optStrategy.equity=}, {optStrategy.orders=}, {optStrategy.position=}, {optStrategy.trades=}")
      logger.info(f"{optStrategy.sma_f=}, {optStrategy.sma_s=}")
      backtest.sma_f = optStrategy.sma_f
      backtest.sma_s = optStrategy.sma_s

      if (PERIOD % PERIOD_GROUP) == 0:
        await send_telegram_doc()
      
      time.sleep(PERIOD_LENGTH_SEC)
      PERIOD += 1

#logger.info(f"{SYMBOL=}, {PERIOD_LENGTH_SEC=}, {PERIODS=}, {PERIOD_GROUP=}, {DATA_STRUCT_CATEGORY=}")
#asyncio.run(loop())

