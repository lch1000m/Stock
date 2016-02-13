import pandas as pd, numpy as np
import pandas.io.data as web
from Stock_Class import *
from Stock_Function import *
import datetime
from dateutil.parser import parse


'''
#########################
# Main Process
#########################
'''

start = '2014-1-1'
end = '2017-1-1'

Raw = read_stock(start=start, end=end)

# Additional Information
Raw.ma(periods=[5])
Raw.bb(periods=[6])
Raw.ma_angle(periods=[60], date_range=5)
Raw.estrangement(periods=[20])


Result = pd.DataFrame(columns= ['Code','Name','Price','MA5','MA20','MA60_angle','BB6','PCT,3days','EST20','PCT,vol'])

for i, st in enumerate(Raw['Name'].unique()):
	temp = Raw[Raw['Name'] == st]

	try:
		Result.set_value(i, 'Code', temp['Code'].unique()[0])
		Result.set_value(i, 'Name', st)
		Result.set_value(i, 'Price', temp.get_value(temp.index[len(temp)-1], 'Close'))
		Result.set_value(i, 'MA5', temp.get_value(temp.index[len(temp)-1], 'MA5'))
		Result.set_value(i, 'MA20', temp.get_value(temp.index[len(temp)-1], 'MA20'))
		Result.set_value(i, 'MA60_angle', temp.get_value(temp.index[len(temp)-1], 'MA60_angle'))
		Result.set_value(i, 'BB6', temp.get_value(temp.index[len(temp)-1], 'BB6'))
		Result.set_value(i, 'PCT,3days', (temp.get_value(temp.index[len(temp)-1], 'Close') - temp.get_value(temp.index[len(temp)-4], 'Close')) / temp.get_value(temp.index[len(temp)-4], 'Close') * 100)
		Result.set_value(i, 'EST20', temp.get_value(temp.index[len(temp)-1], 'EST20'))
		Result.set_value(i, 'PCT,vol', temp['Close'][len(temp)-3:len(temp)].mean() /temp['Close'][len(temp)-3-20:len(temp)-3].mean() * 100)
	except:
		pass

excel(Result)