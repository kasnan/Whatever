# -*- coding: euc-kr -*-

from openpyxl import Workbook
from openpyxl import load_workbook
import datetime
path = './data.xlsx'

wb = Workbook()
sheet1 = wb.active
sheet2 = wb.active

def write_exc(script, logtype):
    wb = Workbook()
    sheet1 = wb.active
    sheet2 = wb.active

    sheet1.title = "TransAction"
    sheet2.title = "Profit"

    if logtype == "BuyCoin" or logtype == "SellCoin":
        sheet1.append([datetime.date.today.isoformat(), ticker, volume, script, logtype])
    elif logtype == "ProfitReport":
        sheet2.append([datetime.date.today.isoformat(), script, logtype])

    wb.save(path)


sheet1.append([1,2,3])
wb.save(path)
