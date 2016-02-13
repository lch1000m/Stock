import pandas as pd, numpy as np
import pandas.io.data as web
from Stock_Class import *
from Stock_Function import *
import datetime

'''
#########################
# Main Process
#########################
'''

start = '2014-1-1'
end = '2015-1-1'

Raw = read_stock(start=start, end=end)

_first = Raw.index.min()
_last = Raw.index.max()

_duration = len(Raw) -1

pct_change = round((Raw.loc[_last, 'Close'] - Raw.loc[_first, 'Close']) / Raw.loc[_first, 'Close'] * 100 / _duration, 1)

from scipy.stats import linregress as lin
Slope = lin(range(len(Raw)), Raw['Close'].values) / Raw['Close'].values.mean() * 100 * 100

Result = pd.DataFrame(columns= ['Code','Name','Date','Duration(d)','Pct','Slope'])

Result.set_value(0, 'Code', Raw['Code'].unique()[0])
Result.set_value(0, 'Name', Raw['Name'].unique()[0])
Result.set_value(0, 'Date', str(_first)[:10] + '->' + str(_last)[:10])
Result.set_value(0, 'Duration(d)', _duration)
Result.set_value(0, 'Pct', pct_change)
Result.set_value(0, 'Slope', Slope[0])

excel(Result, index= False)