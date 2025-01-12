import yfinance as yf
import pandas as pa
import numpy as np

df = yf.download('EUROUSD', start='2021-01-01',interval='1h')
print(df)