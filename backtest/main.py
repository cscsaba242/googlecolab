import ta.momentum
import yfinance as yf
import pandas as pa
import numpy as np
import ta
import pdb

symbol = yf.Ticker('MSFT')
df = yf.download(['MSFT'], start='2024-11-01', interval='1h', auto_adjust=False)

df['stochrsi_k'] = ta.momentum.stochrsi_k(df['Close'].squeeze()) 
df['stochrsi_d'] = ta.momentum.stochrsi_d(df['Close'].squeeze()) 
for i in (8,14,50):
    df['EMA_' + str(i)] = ta.trend.ema_indicator(df['Close'].squeeze(), window = i)

df['atr'] = ta.volatility.average_true_range(df['High'].squeeze(), df['Low'].squeeze(), df['Close'].squeeze())
df.dropna(inplace=True)

def checkCross(data_frame):
    series = data_frame['stochrsi_k'] > data_frame['stochrsi_d']
    return series.diff()

df['cross'] = checkCross(df)
df['TP'] = df['Close'].squeeze() + df['atr'] * 2
df['SL'] = df['Close'].squeeze() - df['atr'] * 3

df['buy_signal'] = np.where((df['cross']) & (df['Close'].squeeze() > df['EMA_8']) & (df['EMA_8'] > df['EMA_14']) & (df['EMA_14'] > df['EMA_50']), 1, 0)

selldates=[]
outcome=[]
cols = ['buy_signal', 'outcome', 'sell_signal']

print(df['buy_signal'])
for i in range(len(df)):
    if df.buy_signal.iloc[i]:
        k = 1
        SL = df.SL.iloc[i]
        TP = df.TP.iloc[i]
        in_position = True
        while in_position:
            if k + i >= len(df):
                break
            looping_close = df.Close.iloc[i + k]
            if looping_close.squeeze() >= TP:
                selldates.append(df.iloc[i+k])
                outcome.append('TP')
                in_position = False
            elif looping_close.squeeze() <= SL:
                selldates.append(df.iloc[i+k])
                outcome.append('SL')
                in_position = False
            k += 1

#            if i + k >= len(df):
#                break
#            looping_high = df.High.iloc[i + k]
#            looping_low = df.Low.iloc[i + k]
#            if looping_high.squeeze() >= TP:
#                selldates.append(df.iloc[i + k].name)
#                outcome.append('TP')
#                in_position = False
#            elif looping_low.squeeze() <= SL:
#                selldates.append(df.iloc[i + k].name)
#                outcome.append('SL')
#                in_position = False
#            k +=1


df.loc[selldates, 'sell_signal'] = 1
df.loc[selldates, 'outcome'] = outcome

df.sell_signal = df.sell_signal.fillna(0).astype(int)

mask = df[(df.buy_signal == 1) | (df.sell_signal == 1) ]
mask2 = mask[(mask.buy_signal.diff() == 1) | (mask.sell_signal.diff() == 1) ]
#print(mask2[['sell_signal','buy_signal','outcome']])
#mask2.outcome.value_counts()
#print(mask2[['sell_signal','buy_signal','outcome']])
mask2.value_counts()