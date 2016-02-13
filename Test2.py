
import pandas as pd
from os import listdir
from Stock_Class import *
from Stock_Function import *



StockList = pd.read_excel(r'C:\Users\Administrator\PycharmProjects\Stock\Input\KOSPI Code.xlsx', sheetname='Code')
StockList['Code_new'] = StockList['Name'] + ' ' + StockList['Code'] + '.txt'


Total = pd.DataFrame()

for i, cd in enumerate(StockList['Code_new']):
    print(i, cd)

    try:
        Raw = read_DB(Code= cd, start='2015-6-20', end= '2017-1-1')

        Raw.estrangement(column='Close', periods=[5,20])
        Raw.bb(column='Close', periods=[6])

        Raw['MA5-MA20 Skew'] = Raw['EST_Close_20'] - Raw['EST_Close_5']

        Total = zipping(Total, Raw.tail(1))

    except:
        pass




Total.sort_values(['MA5-MA20 Skew'], ascending=True, inplace=True)

excel(Total)


beep()