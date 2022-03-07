# -*- coding: euc-kr -*-

import os
import time
from numpy import float64
import pyupbit
import pandas as pd


# 업비트 access key, secret key 변수
upbit_access = "GxSdhgc2FodHTpSKKlwGmUWBUDD3fUzH5HcESvc6"
upbit_secret = "ri1rd0AjgTLVN99o3X1XxySRBj23uxv9Hp0ROqdu"

# 코인 리스트
tickers = []
# 원화로 매매 가능한 코인 리스트 만들기
tickers = pyupbit.get_tickers(fiat="KRW")

# volatility breakout
def cal_target(ticker):
    btc = pyupbit.get_ohlcv(ticker, interval='day', count=10)

    df = pd.DataFrame(data=btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['range'] = (df['high'] - df['low']) * 0.5
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)

    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    long_target = today['open'] + (yesterday['high'] - yesterday['low']) * 0.5
    short_target = today['open'] - (yesterday['high'] - yesterday['low']) * 0.5
    #print(float(target))
    return long_targett, short_target