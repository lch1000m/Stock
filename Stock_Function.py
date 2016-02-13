import pandas as pd
import numpy as np


def read_DB(Code=[], start= None, end= None, sampling= 'D'):
    """
    Read stock raw information from DB (PC)
    """
    from Stock_Class import Stocka

    if start is None:
        start = '2015-1-1'
    if end is None:
        end = '2017-12-31'

    StockRaw = pd.read_table(joinpath(r'C:\Users\Administrator\PycharmProjects\Stock\DB', Code))
    StockRaw['Date'] = pd.to_datetime(StockRaw['Date'])
    StockRaw.set_index(['Date'], inplace=True)

    StockRaw = StockRaw.ix[start:end]

    return Stock(StockRaw)



def joinpath(*args):
    from os.path import join

    for i in range(len(args)):
        if i == 0:
            path =args[i]
        else:
            path = join(path, args[i])

    return path


def excel(Df, index=True):

    """
    Save DataFrame to excel format

    :param Df: DataFrame to save
    :param index: index field is included or not
    """

    writer = pd.ExcelWriter(r'C:\Users\Administrator\PycharmProjects\Stock\Output\Output.xlsx', engine='xlsxwriter')
    Df.to_excel(writer, sheet_name='Sheet1', index= index)


def csv(Df, index= True):

    """
    Save DataFrame to csv format

    :param Df: DataFrame to save
    :param index: index field is included or not
    """
    Df.to_csv(r'C:\Users\Administrator\PycharmProjects\Stock\Output\Output.txt', index= index, sep= '\t')


def volume_check(Df, long_periods= 60, short_periods= 1):

    """
    Stock Volume comparison between short periods over long periods

    :param Df: DataFrame which contains stock volume information
    :param long_periods: long period [int]
    :param short_periods: short period [int]
    :return:
    """

    today = Df.index.max()

    _short_periods = pd.bdate_range(end= today, periods= short_periods)
    _long_periods = pd.bdate_range(end= today, periods= long_periods)

    sample = Df[Df.index.isin(_long_periods)]

    _long_periods = _long_periods - _short_periods

    sample.loc[sample.index.isin(_short_periods), 'Section'] = 'New'
    sample.loc[sample.index.isin(_long_periods), 'Section'] = 'Old'

    pivot = pd.pivot_table(sample, index= ['Code','Name'], columns= ['Section'], values= 'Volume', aggfunc= np.mean)
    pivot['Date Duration [Day]'] = str(long_periods) + ' vs. ' + str(short_periods)
    pivot['Volume PCT'] = pivot['New'] / pivot['Old'] * 100

    pivot['Rank'] = pivot['Volume PCT'].rank(method= 'first', ascending= False)
    pivot.sort_values(by = ['Rank'], ascending= True, inplace= True)

    return pivot



def profit_margin(Df, period_range= 20):

    Summary = pd.DataFrame(columns= ['Name','Date','Period','Min','Max','Min pct','Max pct','Price start','Price end','Price pct','Min-Max Range'])

    for i, st in enumerate(Df['Name'].unique()):
        try:
            temp = Df[Df['Name'] == st]

            end = temp.index[len(temp) -1]
            start = temp.index[len(temp) -1 -period_range]

            Sample = temp.ix[start: end]
            Sample.set_index([Sample.index,'Code','Name','Volume'], inplace= True)

            Sample = Sample.stack().reset_index()
            Sample.rename(columns= {'level_3':'Category', 0:'Price'}, inplace= True)

            Summary.set_value(i, 'Name', Sample['Name'].ix[0])
            Summary.set_value(i, 'Date', str(start)[:10] + '->' + str(end)[:10])
            Summary.set_value(i, 'Period', period_range)
            Summary.set_value(i, 'Min', Sample['Price'].min())
            Summary.set_value(i, 'Max', Sample['Price'].max())
            Summary.set_value(i, 'Min pct', round((- temp.get_value(start, 'Close') + Sample['Price'].min()) / temp.get_value(start, 'Close') * 100, 1))
            Summary.set_value(i, 'Max pct', round((- temp.get_value(start, 'Close') + Sample['Price'].max()) / temp.get_value(start, 'Close') * 100, 1))
            Summary.set_value(i, 'Price start', temp.get_value(start, 'Close'))
            Summary.set_value(i, 'Price end', temp.get_value(end, 'Close'))
            Summary.set_value(i, 'Price pct', round((temp.get_value(end, 'Close') - temp.get_value(start, 'Close')) / temp.get_value(start, 'Close') *100, 1))
            Summary['Min-Max Range'] = Summary['Max pct'] - Summary['Min pct']

        except:
            pass

    return Summary



def read_stock(code= 'all', engine= 'yahoo',start= None, end= None, sampling= 'D'):
    """
    Read stock raw information from server

    :param code: stock names to extract from KOSPI excel file
    :param engine: DB server to extract. Ex) 'yahoo', 'google'
    :param start: start day. Ex) '2013-1-1'
    :param end: end day. Ex) '2016-5-23'
    :param sampling: Sampling date interval. Ex) D: day, W: week, y: year
    :return: DataFrame of stock information. Valid columns are Open,High,Low,Close,Volume,Adj_Close
    """

    from Stock_Class import Stock
    import pandas.io.data as web

    if start is None:
        start = '2015-1-1'
        end = '2016-12-31'

    if code == 'all':
        StockList = pd.read_excel(r'C:\Users\Administrator\PycharmProjects\Stock\Input\KOSPI Code.xlsx', sheetname= 'Code', dtypes= {'Code':str})
        code = StockList['Code'].values
        name = StockList['Name'].values

    Df = pd.DataFrame()

    for i, st in enumerate(code):
        try:
            print(i,'-',st)
            if engine == 'google':
                st = str(st).replace('.KS','')
            temp = web.DataReader(st, engine, start, end)
            temp = temp[temp['Volume'] != 0]
            temp['Code'] = str(st)
            temp['Name'] = name[i]

            Df = zipping(Df, temp)

        except:
            pass

    if sampling != 'D':
        Df = Df.resample(sampling)

    return Stock(Df)



def zipping(Df1, Df2):

    """
    Two DataFrane concatenate along vertical direction

    :param Df1: Original DataFrame to join
    :param Df2: Concatenated DataFrame
    :return: Concatenated DataFrame including Df1, Df2
    """
    if Df1.empty:
        return Df2
    else:
        return pd.concat([Df1,Df2])



def beep(freq=400, duration=1000):

    """
    Make sound from given frequency & duration
    """
    from winsound import Beep
    Beep(freq,duration)