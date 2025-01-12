#!/bin/bash

#INSTALL
python -m venv . 
source ./bin/activate
python -m ensurepip --upgrade
python -m pip install numpy pandas yfinance ta
source ./bin/activate