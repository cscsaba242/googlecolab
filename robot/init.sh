#!/bin/sh
#sudo yum -y install git
#git clone https://github.com/cscsaba242/googlecolab.git
#git config --global user.email "cscsaba242@live.com"
#git config --global user.name "Csaba AWS"
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