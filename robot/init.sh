#!/bin/sh
#sudo yum -y install git
#git config --global user.email "cscsaba242@live.com";git config --global user.name "Csaba AWS";git clone https://github.com/cscsaba242/googlecolab.git

python3 -m venv .
source ./bin/activate
python3 -m ensurepip --upgrade
python3 -m pip install pybit
python3 -m pip install --upgrade pybit
python3 -m pip install pandas
python3 -m pip install pandas-ta
python3 -m pip install backtesting
python3 -m pip install python-telegram-bot
python3 -m pip install asyncio
yes | cp squeeze_pro.py /home/ec2-user/googlecolab/robot/lib64/python3.9/site-packages/pandas_ta/momentum

#'2024-11-02 21:18:32,655 - INFO - loop - DF.size=1215'
#/home/ec2-user/googlecolab/robot/robo.py:150: UserWarning: Some prices are larger than initial cash value. Note that fractional trading is not supported. If you want to trade Bitcoin, increase initial cash, or trade μBTC or satoshis instead (GH-134).
#  backtest = Backtest(DF, SmaCross,cash=10000*comp, commission=.002,exclusive_orders=True)
#/home/ec2-user/googlecolab/robot/robo.py:150: UserWarning: Data index is not datetime. Assuming simple periods, but `pd.DateTimeIndex` is advised.
#  backtest = Backtest(DF, SmaCross,cash=10000*comp, commission=.002,exclusive_orders=True)
#/home/ec2-user/googlecolab/robot/lib64/python3.9/site-packages/backtesting/backtesting.py:1384: FutureWarning: The behavior of Series.idxmax with all-NA values, or any-NA and skipna=False, is deprecated. In a future version this will raise ValueError
#  best_params = heatmap.idxmax()
#'2024-11-02 21:18:32,831 - INFO - loop - optStrategy.equity=1000000, optStrategy.orders=(), optStrategy.position=<Position: 0 (0 trades)>, optStrategy.trades=()'
#'2024-11-02 21:18:32,831 - INFO - loop - optStrategy.sma_f=5, optStrategy.sma_s=10'
#^CTraceback (most recent call last):