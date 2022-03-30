# -*- coding: euc-kr -*-

import os
import time
from numpy import float64
import pyupbit
import pandas as pd
import numpy as np

def get_ror(ticker, k):
    df = pyupbit.get_ohlcv(ticker)

    try:
        
        df['range'] = (df['high'] - df['low']) * 0.5
        df['range_shift1'] = df['range'].shift(1)
        df['target'] = df['open'] + df['range'].shift(1)
        
        fee = 0.005
        df['ror'] = np.where(df['high'] > df['target'],
                           df['close'] / df['target'] - fee,
                           1)

        ror = df['ror'].cumprod()[-2]
    except:
        return 0
    return ror

def get_k(ticker):
    maximum_k = 0; maximum_ror = -9999
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(ticker, k)
        if maximum_ror <= ror:
            maximum_ror = ror
            maximum_k = k
    return maximum_k

# volatility breakout
def cal_target(ticker):
    tic = pyupbit.get_ohlcv(ticker, interval='day', count=21)

    df = pd.DataFrame(data=tic, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['range'] = (df['high'] - df['low']) * 0.5
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)

    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    
    l = 0
    try:
        k = get_k(ticker)
        l = k
    except:
        l=0.5
    print(f"proper k value : { l }")
    long_target = today['open'] + (yesterday['high'] - yesterday['low']) * l
    short_target = today['open'] - (yesterday['high'] - yesterday['low']) * l
    #print(float(target))
    return long_target, short_target

def cal_tickscal(ticker):
    now_price = pyupbit.get_current_price(ticker)

    if now_price >= 2000000:
        tick = 1000
        scale = -3

    elif now_price >= 1000000:
        tick = 500
        scale = -2
    
    elif now_price >= 500000:
        tick = 100
        scale = -2

    elif now_price >= 100000:
        tick = 50
        scale = -1

    elif now_price >= 10000:
        tick = 10
        scale = -1

    elif now_price >= 1000:
        tick = 5
        scale = 0

    elif now_price >= 100:
        tick = 1
        scale = 0

    elif now_price >= 10:
        tick = 0.1
        scale = 1

    else:
        tick = 0.01
        scale = 2

    return tick, scale