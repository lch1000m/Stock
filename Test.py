import win32com.client
from Stock_Class import *
from Stock_Function import *
import time
import win32com.client
import pandas as pd


# Input Parameter ##########################
separator = 5000
timesleep = 5

Request_Dates = 2880
# Input Parameter ##########################



StockList = pd.read_excel(r'C:\Users\Administrator\PycharmProjects\Stock\Input\KOSPI Code.xlsx', sheetname='Code')

Stockdict = {}

for i in range(len(StockList)):
    Stockdict[StockList['Code'].values[i]] = StockList['Name'].values[i]



Df_Final = pd.DataFrame()

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

    Df.sort_values(['Date'], ascending=True, inplace=True)
    Df = Stock(Df)


    '''
    #############################################################
    # Add Calculation Analysis part
    #############################################################
    '''
    '''
    Df.ma_angle(column='Close', periods= [5,20,60])
    Df.estrangement(column='Close', periods= [5,20])
    Df.bb(column='Close', periods=[6])
    Df.bb(column='Low', periods=[6])
    Df.bb(column='High', periods=[6])

    print(Df.tail(10))
    '''
    '''
    #############################################################
    # Add Calculation Analysis part
    #############################################################
    '''

    Df_Final = zipping(Df_Final, Df)

    NumofStock += 1
    print('Number of Stock Processed', NumofStock)

    if (NumofStock % separator == 0) and (NumofStock >= separator):
        print('Its time to sleep :', timesleep)
        time.sleep(timesleep)

# Data type conversion
Df_Final['Date'] = pd.to_datetime(Df_Final['Date'])

for col in ['Open','High','Low','Close','Volume']:
    Df_Final[col] = Df_Final[col].astype(float)

print(Df.info())
print(Df.head())
print(Df.tail())














'''
##########################
종목 Code, Name 얻기
##########################

instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = instCpCodeMgr.GetStockListByMarket(0)    # 1:KOSPI, 2:KOSDAQ


StockInfo = pd.DataFrame(columns= ['Code','Name'])

_idx = 0

for market in [1,2]:
    codeList = instCpCodeMgr.GetStockListByMarket(market)

    for code in codeList:
        StockInfo.set_value(_idx, 'Code', code)
        StockInfo.set_value(_idx, 'Name', instCpCodeMgr.CodeToName(code))
        print(market, code, instCpCodeMgr.CodeToName(code))

        _idx += 1

excel(StockInfo)
'''