import ta.momentum
import yfinance as yf
import pandas as pa
import numpy as np
import ta

symbol = yf.Ticker('MSFT')
df = yf.download(['MSFT'], start='2025-01-01', interval='1h', auto_adjust=False)
#print(df['Close'].shape)
#print(type(df['Close']))
#print(df.head())
#df.xs('MSFT', axis=1, level='Ticker')
df['stochrsi_k'] = ta.momentum.stochrsi_k(df['Close'].squeeze()) 
df['stochrsi_d'] = ta.momentum.stochrsi_d(df['Close'].squeeze()) 
for i in (8,14,50):
    df['EMA_' + str(i)] = ta.trend.ema_indicator(df['Close'].squeeze(), window = i)

df['atr'] = ta.volatility.average_true_range(df['High'].squeeze(), df['Low'].squeeze(), df['Close'].squeeze())
df.dropna(inplace=True)
#print(symbol.info)
#df = yf.download('EUROUSD', start='2022-01-01',interval='1h')
def checkCross(data_frame):
    series = data_frame['stochrsi_k'] > data_frame['stochrsi_d']
    return series.diff()

df['cross'] = checkCross(df)
df['TP'] = df['Close'].squeeze() + df['atr'] * 2
df['SL'] = df['Close'].squeeze() - df['atr'] * 3

df['Buysignal'] = np.where((df['cross'] == 1) & (df['Close'].squeeze() > df['EMA_8']) & (df['EMA_8'] > df['EMA_14']) & (df['EMA_14'] > df['EMA_50']), 1, 0)

selldates=[]
outcome=[]

for i in range(len(df)):
    if df['Buysignal'].iloc[i]:
        k = 1
        SL = df['SL'].iloc[i]
        TP = df['TP'].iloc[i]
        inposition = True
        while inposition:
            looping_close = df['Close'].squeeze().iloc[i + k]
            if looping_close >= TP:
                selldates.append(df.iloc[i + k].name)
                outcome.append('TP')
                inposition = False
            elif looping_close <= SL:
                selldates.append(df.iloc[i + k].name)
                outcome.append('SL')
                inposition = False
            
            k += 1


print(df)

