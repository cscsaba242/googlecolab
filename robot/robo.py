import requests
from datetime import datetime, timedelta
import time
import os
import json
import pandas
import pandas_ta as ta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import telegram as tg
import asyncio
import ipdb
import logging

#Start,End,Duration,Exposure Time [%],Equity Final [$],Equity Peak [$],Return [%],
#Buy & Hold Return [%],Return (Ann.) [%],Volatility (Ann.) [%],Sharpe Ratio,Sortino Ratio
#Calmar Ratio,Max. Drawdown [%],Avg. Drawdown [%],Max. Drawdown Duration,Avg. Drawdown Duration,# Trades
#Win Rate [%],Best Trade [%],Worst Trade [%],Avg. Trade [%],Max. Trade Duration,Avg. Trade Duration
#Profit Factor,Expectancy [%],SQN,_strategy,_equity_curve,_trades

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

minsBackMax=1000
# 10,05 16:23 1728145380000 18:23 1728152580000
# 10,05 20:22 o:61920.30 h:61961.80 l:61920.30
# start = datetime.strptime("2024 10 05, 16:23:00", "%Y %m %d, %H:%M:%S").timestamp()
# start = int(round(start * 1000))
#getUpdates response:
#{'ok': True, 'result': [{'update_id': 3987255, 'message': {'message_id': 2, 'from':
#{'id': 5833186787, 'is_bot': False, 'first_name': 'bunnypussylover', 'username': 'bunnypussylover', 'language_code': 'en'},
#'chat': {'id': 5833186787, 'first_name': 'bunnypussylover', 'username': 'bunnypussylover', 'type': 'private'}, 'date': 1728931474, 'text': 'hi'}}]}
payload={};
headers = {'User-Agent': 'Mozilla/5.0'}
cols=['Date','Open','High','Low','Close']
DF=pandas.DataFrame()
bot=tg.Bot(token=token)
comp=100
DOC_FILE="./doc.txt"
IMG_FILE="./image.jpg"
PERIOD=5 #period in sec
PERIODS=2  # periods in PERIOD
PERIOD_GROUP=1 #period to send message

async def send_telegram_image():
	global bot
	global chat_id
	with open('./image.jpg', 'rb') as photo:
		await bot.send_photo(chat_id=chat_id, photo=photo)

async def send_telegram_doc():
        global bot
        global chat_id
        with open(DOC_FILE, 'rb') as doc:
                await bot.send_document(chat_id=chat_id, document=doc)

def get_telegram_info():
	global token
	url = f"https://api.telegram.org/bot{token}/getUpdates"
	response = requests.get(url)

def write_doc(text):
	with open(DOC_FILE, 'a') as file:
    		file.write(text)

def clear_doc():
  open(DOC_FILE, 'w').close()

class SmaCross(Strategy):
  sma_f = 10
  sma_s = 20
  sma_f_func = None
  sma_s_func = None

  def init(self):
    close = self.data.Close
    self.sma_f_func = self.I(SMA, close, self.sma_f)
    self.sma_s_func = self.I(SMA, close, self.sma_s)

  def next(self):
    if crossover(self.sma_f_func, self.sma_s_func):
      self.buy()
    elif crossover(self.sma_s_func, self.sma_f_func):
      self.sell()

def convNum(dfParam: pandas.Series):
	return (pandas.to_numeric(dfParam)*100).astype(int)


def getPrices(categoryParam, symbolParam, limitParam, colsParam):
  global logger
  global headers
  global payload

  lf=pandas.DataFrame()
  url = f"https://api-testnet.bybit.com/v5/market/mark-price-kline?category={categoryParam}&symbol={symbolParam}&interval=1&limit={limitParam}"
  resp=requests.request("GET", url, headers=headers, data=payload)
  print(resp)

	#lf=pandas.DataFrame(resp["result"]["list"], columns=colsParam)
	#lf['Date'] = pandas.to_datetime(lf['Date'], unit='ms')
	#lf['Open'] = convNum(lf['Open'])
	#lf['High'] = convNum(lf['High'])
	#lf['Low'] = convNum(lf['Low'])
	#lf['Close'] = convNum(lf['Close'])

	#respCode=resp["retCode"]; respMsg=resp["retMsg"]; respCat=resp["result"]["category"];respSymb=resp["result"]["symbol"]
	#result = f"request result code: {respCode}, msg: {respMsg}, cat: {respCat}, symb: {respSymb}"
	#return [lf, result]
  #return [lf, "test"]

def main():
  global DF
  global PERIOD_GROUP
  global logger

  limit=200 if DF.empty else PERIOD_GROUP
  ret = getPrices("linear", "BTCUSDT", limit, cols)
  logger.info(f"get prices: {ret}")
  #lf = ret[0]
  #retMessage = ret[1]

  #if DF.empty:
  #  DF=lf.copy()
  #else:
  #  DF = pandas.concat([lf,DF], ignore_index=True)
  #return retMessage

def loop():
  p=0
  global DF
  global chat_id
  global PERIOD
  global PERIODS
  global PERIOD_GROUP
  #clear_doc()

  while p < PERIODS:
    main()
    #ipdb.set_trace()
    #write_doc(f"candles import: {candles_import}, size:{DF.size}")
    #backtest = Backtest(DF, SmaCross,cash=10000*comp, commission=.002,exclusive_orders=True)
    #backtestOptimized=backtest.optimize(sma_f=[5, 10, 15], sma_s=[10, 20, 40], constraint=lambda p: p.sma_f < p.sma_s)
    #optStrategy = backtestOptimized._strategy
    #write_doc(f"Opt. equity:{optStrategy.equity}\n")
    #write_doc(f"Opt. orders:{optStrategy.orders}\n")
    #write_doc(f"Opt. position:{optStrategy.position}\n")
    #write_doc(f"Opt. trades:{optStrategy.trades}\n")
    #optStrategy = backtestOptimized._strategy
    #backtest.sma_f=optStrategy.sma_f
    #backtest.sma_s=optStrategy.sma_s

    #if (p % PERIOD_GROUP) == 0:
			#await send_telegram_doc()
      #clear_doc()
    logger.info("period:" + str(p))
    time.sleep(PERIOD)
    p+=1
loop()
