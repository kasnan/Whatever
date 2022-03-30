# -*- coding: euc-kr -*-

import pyupbit
import numpy as np

def get_hpr(year, month, ticker):
    try:
        df = pyupbit.get_ohlcv(ticker)
        df = df[str(year)][str(month)]
        
        df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
        df['range'] = (df['high'] - df['low']) * 0.5
        df['target'] = df['open'] + df['range'].shift(1)
        df['bull'] = df['open'] > df['ma5']
 
        fee = 0.005
        df['ror'] = np.where((df['high'] > df['target']) & df['bull'],
                               df['close'] / df['target'] - fee,
                               1)
 
        df['hpr'] = df['ror'].cumprod()
        df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
        return df['hpr'][-2]
    except:
        return 1

def getsorted_hpr(year, month):
    tickers = pyupbit.get_tickers(fiat="KRW")
    hprs = []
    for ticker in tickers:
        hpr = get_hpr(year, month, ticker)
        hprs.append((ticker, hpr))
    sorted_hprs = sorted(hprs, key=lambda x:x[1], reverse=True)
    print(sorted_hprs[:5])
    return sorted_hprs[:3]

def bull_market(ticker):
    df = pyupbit.get_ohlcv(ticker)
    ma5 = df['close'].rolling(window=5).mean()
    last_ma5 = ma5[-2]

    price = pyupbit.get_current_price(ticker)
    if price > last_ma5:
        return True
    else:
        return False