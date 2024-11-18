from get_prices import GetPrices
from pandas import DataFrame

class ByBit(GetPrices):
  CATEGORY = "linear"

  async def do(self, interval:str, symbol:str, DT_from: datetime, DT_to:datetime) -> DataFrame:
    self.logger.info(f"ByBit.do: {symbol=}, {interval=}, {DT_from=}, {DT_to=}")
    lf=DataFrame()
    url = f"https://api-testnet.bybit.com/v5/market/mark-price-kline?category={self.CATEGORY}&symbol={symbol}&interval={interval}&limit={limitParam}&start={start}&end={end}"
    resp=requests.request("GET", url, headers=self.headers, data=self.payload).json()
}
    lf = pandas.DataFrame(resp["result"]["list"], columns=self.COLS)
    lf['Date'] = pandas.to_datetime(lf['Date'].astype(float))
    lf['Open'] = self.convNum(lf['Open'])
    lf['High'] = self.convNum(lf['High'])
    lf['Low'] = self.convNum(lf['Low'])
    lf['Close'] = self.convNum(lf['Close'])

    self.logger.info(f"ByBit.do: {lf.size=}, {resp['retCode']=}, {resp['retMsg']=}")
    return lf
  
  pass