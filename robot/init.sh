#!/bin/sh
#sudo yum -y install git
#git config --global user.email "cscsaba242@live.com"
#git config --global user.name "Csaba AWS"
python3 -m venv .
source ./bin/activate
python3 -m ensurepip --upgrade
python3 pip install pybit
python3 pip install --upgrade pybit
python3 pip install pandas
python3 pip install pandas-ta
python3 pip install backtesting
python3 pip install python-telegram-bot
python3 pip install asyncio