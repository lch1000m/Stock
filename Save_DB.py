import win32com.client
from Stock_Class import *
from Stock_Function import *
import time
import win32com.client
import pandas as pd

from datetime import datetime as dt

# Add new line

# Input Parameter ##########################
separator = 5
timesleep = 2

Request_Dates = 1    # 2880
# Input Parameter ##########################


start = dt.now()



StockList = pd.read_excel(r'C:\Users\Administrator\PycharmProjects\Stock\Input\KOSPI Code.xlsx', sheetname='Code')

Stockdict = {}

for i in range(len(StockList)):
    Stockdict[StockList['Code'].values[i]] = StockList['Name'].values[i]



Df = pd.DataFrame()

NumofStock = 0

for codelist in StockList['Code'].values:

    instStockChart = win32com.client.Dispatch('CpSysDib.StockChart')

    # SetInputValue
    instStockChart.SetInputValue(0, codelist)
    instStockChart.SetInputValue(1, ord('2'))
    instStockChart.SetInputValue(4, Request_Dates)
    instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8))
    instStockChart.SetInputValue(6, ord('D'))

    # BlockRequest
    instStockChart.BlockRequest()

    # GetHeaderValue
    numData = instStockChart.GetHeaderValue(3)  # Number of Row
    numFiled = instStockChart.GetHeaderValue(1)    # Number of Columns

    # GetDataValue

    ColumnName = ['Date','Open','High','Low','Close','Volume']

    Df = pd.DataFrame(columns=ColumnName)

    key = {}
    for i, val in enumerate(ColumnName):
        key[i] = val


    for i in range(numData):
        for j in range(numFiled):
            Df.set_value(i, key[j], instStockChart.GetDataValue(j, i))

    Df['Code'] = codelist
    Df['Name'] = Stockdict[codelist]

    # Datetime change
    Df['Date'] = 'A' + Df['Date'].astype(str)
    Df['Date'] = Df['Date'].str[1:5] + '-' + Df['Date'].str[5:7] + '-' + Df['Date'].str[7:9]


    NumofStock += 1
    print('Number of Stock Processed', NumofStock)

    Df['Date'] = pd.to_datetime(Df['Date'])

    # Data type conversion
    for col in ['Open','High','Low','Close','Volume']:
        Df[col] = Df[col].astype(float)


    DataBase = pd.read_table(joinpath(r'C:\Users\Administrator\PycharmProjects\Stock\DB', Df['Name'].unique()[0] + ' ' + Df['Code'].unique()[0] + '.txt'))
    DataBase['Date'] = pd.to_datetime(DataBase['Date'])

    DataBase = zipping(DataBase, Df)
    DataBase.drop_duplicates(subset=['Date'], keep='first', inplace=True)
    DataBase.sort_values(['Date'], ascending=True, inplace=True)


    DataBase.to_csv(joinpath(r'C:\Users\Administrator\PycharmProjects\Stock\DB', Df['Name'].unique()[0] + ' ' + Df['Code'].unique()[0] + '.txt'), index=False, sep='\t', encoding='utf-8')

    if (NumofStock % separator == 0) and (NumofStock >= separator):
        print('Its time to sleep :', timesleep)
        time.sleep(timesleep)


end = dt.now()

TotalTime = end - start


print('Total Time :', TotalTime)

beep()