import pandas as pd, numpy as np
import pandas.io.data as web
from Stock_Class import *
from Stock_Function import *
import datetime

#### Input Parameter ##########
start = '2015-1-1'
end = '2017-1-1'
start_plot = '2015-8-1'

Price_to_pct = True

MA_percentile = 0.8
BB_Sigma_Criteria = 1
#### Input Parameter ##########


'''
#########################
# Main Process
#########################
'''

Raw = read_stock(start= start, end= end)

if Price_to_pct == True:
    Raw['Open'] = Raw['Open'] / Raw['Close'].loc[Raw['Close'].index.max()] * 100
    Raw['High'] = Raw['High'] / Raw['Close'].loc[Raw['Close'].index.max()] * 100
    Raw['Low'] = Raw['Low'] / Raw['Close'].loc[Raw['Close'].index.max()] * 100
    Raw['Close'] = Raw['Close'] / Raw['Close'].loc[Raw['Close'].index.max()] * 100


Raw.ma_angle(periods= [5,20,60])
Raw.estrangement(periods= [5,20])
Raw.bb(periods= [6])
Raw['MA60_angle'] = Raw['MA60_angle'].astype(float)

Raw = Raw.ix[start_plot:end]




'''
#########################
# Plot Part
#########################
'''


import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ochl


# Made CandleStock Form
x= 0
y= len(Raw)


CandleAr = []
while x < y:
    temp = []

    temp.append(mdates.date2num(Raw.index[x]))
    temp.append(Raw.loc[Raw.index[x], 'Open'])
    temp.append(Raw.loc[Raw.index[x], 'Close'])
    temp.append(Raw.loc[Raw.index[x], 'High'])
    temp.append(Raw.loc[Raw.index[x], 'Low'])
    temp.append(Raw.loc[Raw.index[x], 'Volume'])

    CandleAr.append(temp)

    x+= 1


# Original Code
fig = plt.figure(facecolor= '#07000d')


# Candle_Raw : Candle Stick
Candle_Raw = plt.subplot2grid((6, 4), (2, 0), rowspan= 3, colspan= 4, axisbg='#07000d')

candlestick_ochl(Candle_Raw, CandleAr, colorup='r', colordown='b', width= .7, alpha= .8)

Candle_Raw.grid(True, color='w')

Candle_Raw.xaxis.set_major_locator(mticker.MaxNLocator(20))
Candle_Raw.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
Candle_Raw.yaxis.label.set_color('w')
Candle_Raw.spines['bottom'].set_color('#5998ff')
Candle_Raw.spines['top'].set_color('#5998ff')
Candle_Raw.spines['left'].set_color('#5998ff')
Candle_Raw.spines['right'].set_color('#5998ff')
Candle_Raw.tick_params(axis='y', colors='w')
Candle_Raw.tick_params(axis='x', colors='w')

for label in Candle_Raw.xaxis.get_ticklabels():
    label.set_rotation(45)

Candle_Raw.plot(Raw.index, Raw['MA5'], color='w', linewidth= 1.2)
Candle_Raw.plot(Raw.index, Raw['MA20'], color='#00ff00', linewidth= 1.2)
Candle_Raw.plot(Raw.index, Raw['MA60'], color='#ffff00', linewidth= 1.2)



# MA20_5_Skew : MA5 - MA20 Delta
MA20_5_Skew = plt.subplot2grid((6, 4), (0, 0), rowspan= 1, colspan= 4, axisbg='#07000d', sharex= Candle_Raw)
MA20_5_Skew.spines['bottom'].set_color('#5998ff')
MA20_5_Skew.spines['top'].set_color('#5998ff')
MA20_5_Skew.spines['left'].set_color('#5998ff')
MA20_5_Skew.spines['right'].set_color('#5998ff')
MA20_5_Skew.tick_params(axis='x', colors='w')
MA20_5_Skew.tick_params(axis='y', colors='w')
MA20_5_Skew.yaxis.label.set_color('w')
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune= 'lower'))
plt.ylabel('MA5-20')
MA20_5_Skew.plot(Raw.index, Raw['EST20'] - Raw['EST5'], color='#00ff00', linewidth= 1.0)
MA20_5_Skew.grid(True, color='w')
MA20_5_Skew.fill_between(Raw.index, Raw['EST20'] - Raw['EST5'], (Raw['EST20'] - Raw['EST5']).quantile(1 - MA_percentile), where=Raw['EST20'] - Raw['EST5'] < (Raw['EST20'] - Raw['EST5']).quantile(1 - MA_percentile), facecolor='#00ff00', alpha= .6)
MA20_5_Skew.fill_between(Raw.index, Raw['EST20'] - Raw['EST5'], (Raw['EST20'] - Raw['EST5']).quantile(MA_percentile), where=Raw['EST20'] - Raw['EST5'] > (Raw['EST20'] - Raw['EST5']).quantile(MA_percentile), facecolor='#00ff00', alpha= .6)
MA20_5_Skew.fill_between(Raw.index, Raw['EST20'] - Raw['EST5'], 0, facecolor='#00ff00', alpha= .15)

plt.setp(MA20_5_Skew.get_xticklabels(), visible= False)

# BB_Sigma : Bollinger Band Sigma
BB_Sigma = plt.subplot2grid((6, 4), (1, 0), rowspan= 1, colspan= 4, axisbg='#07000d', sharex= Candle_Raw)
BB_Sigma.spines['bottom'].set_color('#5998ff')
BB_Sigma.spines['top'].set_color('#5998ff')
BB_Sigma.spines['left'].set_color('#5998ff')
BB_Sigma.spines['right'].set_color('#5998ff')
BB_Sigma.tick_params(axis='x', colors='w')
BB_Sigma.tick_params(axis='y', colors='w')
BB_Sigma.yaxis.label.set_color('w')
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune= 'lower'))
plt.ylabel('BB Close Sigma')
BB_Sigma.plot(Raw.index, Raw['BB6'], color='#ffff1a', linewidth= 1.0)
BB_Sigma.grid(True, color='w')
BB_Sigma.fill_between(Raw.index, Raw['BB6'], -BB_Sigma_Criteria, where=Raw['BB6'] < -BB_Sigma_Criteria, facecolor='#ffff1a', alpha= .6)
BB_Sigma.fill_between(Raw.index, BB_Sigma_Criteria, Raw['BB6'], where=Raw['BB6'] > BB_Sigma_Criteria, facecolor='#ffff1a', alpha= .6)
BB_Sigma.fill_between(Raw.index, Raw['BB6'], 0, facecolor='#ffff1a', alpha= .15)

plt.setp(BB_Sigma.get_xticklabels(), visible= False)



# Volume : Volume information
Volume = Candle_Raw.twinx()
Volume.fill_between(Raw.index, Raw['Volume'].min(), Raw['Volume'], facecolor='#00ffe8', alpha= .5)
Volume.axes.yaxis.set_ticklabels([])
Volume.grid(True, color='w')
Volume.spines['bottom'].set_color('#5998ff')
Volume.spines['top'].set_color('#5998ff')
Volume.spines['left'].set_color('#5998ff')
Volume.spines['right'].set_color('#5998ff')
Volume.set_ylim(0, 2.5 * Raw['Volume'].max())
Volume.tick_params(axis='x', colors='w')
Volume.tick_params(axis='y', colors='w')

plt.ylabel('Stock Price & Volume')



'''
# Add additional Plot
fig2 = plt.figure(facecolor= '#07000d')
ax10 = plt.subplot2grid((5,4), (0,0), rowspan= 1, colspan= 4, axisbg= '#07000d')
ax10.spines['bottom'].set_color('#5998ff')
ax10.spines['top'].set_color('#5998ff')
ax10.spines['left'].set_color('#5998ff')
ax10.spines['right'].set_color('#5998ff')
ax10.tick_params(axis= 'x', colors= 'w')
ax10.tick_params(axis= 'y', colors= 'w')
ax10.xaxis.set_major_locator(mticker.MaxNLocator(20))
ax10.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax10.yaxis.label.set_color('w')
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune= 'lower'))
plt.ylabel('EST20')
ax10.plot(Raw.index, Raw['EST20'], color= '#00ff00', linewidth= 1.0)
ax10.grid(True, color= 'w')
ax10.fill_between(Raw.index, Raw['EST20'], 0, facecolor= '#00ff00', alpha= .5)
'''




plt.subplots_adjust(left= .10, bottom= .0, right= .93, top= .95, wspace= .20, hspace= .0)
#plt.suptitle(Raw['Name'].unique()[0] + 'Stock Price', color= 'w')
plt.xlabel('Date')

plt.show()

beep()