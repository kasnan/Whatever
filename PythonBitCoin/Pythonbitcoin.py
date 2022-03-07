# -*- coding: euc-kr -*-

import time
import pyupbit
from multiprocessing import Process

import MainProcess

idx1 = 0; idx2 = 0; idx3 = 0; idx4 = 0

# 코인 리스트
tickers = []
# 원화로 매매 가능한 코인 리스트 만들기
tickers = pyupbit.get_tickers(fiat="KRW")
lent = len(tickers)

tickers1 = tickers[:int(lent/4)]; tickers2 = tickers[int(lent/4):int(lent/4*2)]
tickers3 = tickers[int(lent/4*2):int(lent/4*3)]; tickers4 = tickers[int(lent/4*3):int(lent/4*4)]

tlist = [tickers1, tickers2, tickers3, tickers4]
ilist = [idx1, idx2, idx3, idx4]

if __name__ == '__main__':
    procs = []

    for i in range(4):
        proc = Process(target=MainProcess.mainp, args=(tlist[i], ilist[i]))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
