# -*- coding: euc-kr -*-

import os
import time
from numpy import double
import datetime
import sys

import pyupbit
from collections import deque
from multiprocessing import Process

import backtest
import BTget
import getCurrentState
global idx
#주문은 초당 8회, 분당 200회 / 주문 외 요청은 초당 30회, 분당 900회 사용 가능합니다.
#업비트 거래수수료는 총 주문금액의 0.05%

# 업비트 access key, secret key 변수

upbit_access = "access key"
upbit_secret = "secret key"
global flag
flag = 0
# 코인 종가 담을 deque 변수
ma20 = deque(maxlen=20)
ma60 = deque(maxlen=60)
ma120 = deque(maxlen=120)

# login
upbit = pyupbit.Upbit(upbit_access, upbit_secret)

# 잔고 조회 krw
def get_balance_krw():    
    balance = upbit.get_balance("KRW")
    return balance
# 잔고 조회 coin
def get_balance_wallet(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker[4:]:
            balance = b['balance']
            avg_buy_price = b['avg_buy_price']
            return float(avg_buy_price), float(balance)
        else:
            pass
    return int(0), int(0)
# 매수 주문
def buy_order(ticker, volume):
    try:
        for i in range(4):
            buy_result = upbit.buy_market_order(ticker=ticker, price=volume)
            if buy_result == None or 'error' in buy_result:
                print("매수 재 주문")
                time.sleep(1)
            else:
                print(ticker+", "+volume+"매수")
                BTget.write_exc(str(ticker+"를 "+volume+"만큼 매수 완료"),"BuyCoin")
                return buy_result
    except Exception as e:
        print(e)
        print("매수 주문 이상")
# 매도 주문
def sell_order(ticker, volume):
    try:
        while True:
            sell_result = upbit.sell_market_order(ticker, volume)
            if sell_result == None or 'error' in sell_result:
                print(f"{sell_result}, 매도 재 주문")
                time.sleep(1)
            else:
                print(ticker+", "+volume+"매도")
                BTget.write_exc(ticker+"를 "+volume+"만큼 매도 완료","SellCoin")
                return sell_result
    except Exception as e:
        print(e)
        print("매도 주문 이상")

# 코인 심볼 하나씩 받아와서 이동평균선 구한 후 매수 조건 탐색
def get_ticker_ma(ticker, unitvolume, mode):  

    '''get_ohlcv 함수는 고가/시가/저가/종가/거래량을 DataFrame으로 반환합니다'''
    df = pyupbit.get_ohlcv(ticker, interval='day', count=21) # 일봉 데이터 프레임 생성
    ma20.extend(df['close'])    # ma20 변수에 종가 넣기
    ma60.extend(df['close'])    # ma60 변수에 종가 넣기
    ma120.extend(df['close'])   # ma120 변수에 종가 넣기
    curr_ma20 = sum(ma20) / len(ma20)       # ma20값 더해서 나누기 = 20일선 이동평균
    curr_ma60 = sum(ma60) / len(ma60)       # ma60값 더해서 나누기 = 60일선 이동평균
    curr_ma120 = sum(ma120) / len(ma120)    # ma20값 더해서 나누기 = 120일선 이동평균

    now_price = pyupbit.get_current_price(ticker)       # 코인의 현재가
    open_price = df['open'][-1]                 # 당일 시가 구하기
    buy_target_price = open_price + (open_price * 0.015) # 목표가 = 당일 시가 보다 2프로 이상 상승 금액
    long_volt_target_price, short_volt_target_price = getCurrentState.cal_target(ticker)

    tick, scale = getCurrentState.cal_tickscal(ticker)

    coin_check = get_balance_wallet(ticker) # 코인 보유 하고 있는지 체크
    avg_price = coin_check[0]   # 매수 평균가
    balance = coin_check[1]     # 코인 보유 개수

    if avg_price == 0 and balance == 0:
        flag = 0
    else:
        flag = 1
    timenow = str(datetime.datetime.now())
    print("(현재시간 : "+timenow+")")
    print(ticker + '시세 감시 중')

    # 볼륨만큼 매수

    volume = round(unitvolume * 0.995, scale)
    if flag == 0 and (mode == 'b' or mode == 'n'):
        if long_volt_target_price <= now_price and flag == 0:
            buy_order(ticker, volume)
            BTget.write_exc("코인명: {}, 구입량: {}%".format(ticker, volume),"BuyCoin")
            flag = 1

        elif short_volt_target_price >= now_price and flag == 0:
            buy_order(ticker, volume)
            BTget.write_exc("코인명: {}, 구입량: {}%".format(ticker, volume),"BuyCoin")
            flag = 1
    
        elif curr_ma20 <= curr_ma60 and curr_ma60 <= curr_ma120 and buy_target_price <= now_price and flag == 0:
            buy_order(ticker, volume)
            BTget.write_exc("코인명: {}, 구입량: {}%".format(ticker, volume),"BuyCoin")
            flag = 1
        pass
    elif flag == 1 and (mode == 's' or mode == 'n'):
        if flag == 1:
            # 현재 보유 코인 수익률 계산 
            buy_profit = ((now_price - avg_price) / avg_price) * 100
            profit = round(buy_profit, 4)
            # 평균 매수가 보다 0.5% 상승 시 매도
            if profit >= 2.5:
                print(f"{ticker} : 목표가 도달 후 전량 매도")
                sell_order(ticker, balance)
                BTget.write_exc("코인명: {}, 판매량: {}%".format(ticker, balance),"SellCoin")
                flag = 0
                if mode == 's':
                    sys.exit()
                return 0 
            else:
                print("코인명: {}, 수익률: {}%".format(ticker, profit))
                BTget.write_exc("코인명: {}, 수익률: {}%".format(ticker, profit),"ProfitReport")
                flag = 0
                return 0
        else:

            print("Nothing!!")
            return 0
            
# 코인 리스트에서 이동 평균선 함수로 하나씩 꺼내서 보내기
def mainp(tickers, idx, mode):
    idx = 0
    
    while True:
        try:
            unitvolume = 500000
            for i in range(len(tickers)):
                print("================================================")
                index = (i+idx)%len(tickers)
                get_ticker_ma(tickers[index],unitvolume, mode)
                
                time.sleep(0.7)
                os.system('cls')
        except Exception as e:
            idx = (idx+1)%len(tickers)
            print(e)
            print("pass")
            pass
