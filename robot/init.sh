#!/bin/sh
#sudo yum -y install git
#git config --global user.email "cscsaba242@live.com";git config --global user.name "Csaba AWS";git clone https://github.com/cscsaba242/googlecolab.git
python -m venv 
source ./bin/activate
python -m ensurepip --upgrade
python -m pip install pybit pandas pandas-ta pyyaml requests pytz backtesting sqlalchemy asyncio

#yes | cp squeeze_pro.py ./lib64/python3.12/site-packages/pandas_ta/momentum
