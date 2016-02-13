import pandas as pd
import numpy as np
from Stock_Function import zipping


class Stock(pd.DataFrame):


    def bb(self, column='Close', periods=[5,20], inplace=True):
        """
        Bollinger Band Sigma from given periods

        :param column: column for calculation -> Open, High, Low, Close
        :param periods: given periods -> [list]
        :param inplace: inplace or not -> True, False
        :return: columns of Bollinger Band Sigma information
        Ex) 1.5, -1.5 : 1.5 & -1.5 Sigma respectively
        """

        if inplace:
            new_obj = self

        new_obj.ma(column=column, periods=periods)
        new_obj.ms(column=column, periods=periods)

        for per in periods:
            new_obj['BB_'+column+'_'+str(per)] = (new_obj[column] - new_obj['MA_'+column+'_'+str(per)]) / new_obj['Sigma_'+column+'_'+str(per)]

        if inplace:
            self._update_inplace(new_obj)

        return  self



    def ms(self, column='Close', periods=[5,20], inplace=True):
        """
        Rolling Standard deviation from given periods

        :param periods: given periods -> [list]
        :param inplace: inplace or not -> True, False
        :return:
        Ex) 1.5, -1.5 : 1.5 & -1.5 Sigma respectively
        """

        if inplace:
            new_obj = self

        result = pd.DataFrame()

        _num = 1
        for st in new_obj['Name'].unique():
            print(_num, st, 'BB')
            temp = new_obj[new_obj['Name'] == st]

            for per in periods:
                temp['Sigma_'+column+'_'+str(per)] = pd.rolling_std(temp[column], per)

            result = zipping(result, temp)

            _num += 1

        if inplace:
            self._update_inplace(result)

        return  self



    def price_angle(self, date_range= 5, inplace= True):
        """
        Price Angle calculation from given date range

        :param date_range: date interval range [int]
        :param inplace: inplace or not -> True, False
        :return: Angel per day [Unit: degree/day]
        """
        from scipy.stats import linregress as lin

        if inplace:
            new_obj = self

        if date_range == 'longest':
            date_range = len(new_obj)

        result = pd.DataFrame()

        for st in new_obj['Name'].unique():
            temp = new_obj[new_obj['Name'] == st]

            Res = []
            for k in range(len(temp)):
                if k < date_range-1:
                    Res.append(np.nan)
                else:
                    y = temp['Close'][k-date_range+1:k+1]
                    res = lin(range(date_range), y)

                    Res.append(str(res[0] / y.mean() * 100 * 100))

            try:
                temp['Price'+str(date_range)+'_angle'] = Res
                result = zipping(result, temp)
            except:
                pass


        result['Price'+str(date_range)+'_angle'] = result['Price'+str(date_range)+'_angle'].astype(float)


        # -30 < Slope < 30 : Neutral
        result.loc[(result['Price'+str(date_range)+'_angle'] > -30) & (result['Price'+str(date_range)+'_angle'] < 30), 'Price'+str(date_range)+'_angle_Signal'] = 'Neutral'
        # 30 <= Slope < 80 : Weak
        result.loc[(result['Price'+str(date_range)+'_angle'] >= 30) & (result['Price'+str(date_range)+'_angle'] < 80), 'Price'+str(date_range)+'_angle_Signal'] = 'P-Weak'
        # 80 <= Slope < 300 : Strong
        result.loc[(result['Price'+str(date_range)+'_angle'] >= 80) & (result['Price'+str(date_range)+'_angle'] < 300), 'Price'+str(date_range)+'_angle_Signal'] = 'P-Strong'
        # 300 <= Slope < 500 : Super
        result.loc[(result['Price'+str(date_range)+'_angle'] >= 80) & (result['Price'+str(date_range)+'_angle'] < 300), 'Price'+str(date_range)+'_angle_Signal'] = 'P-Super'
        # 500 <= Slope : Ultra
        result.loc[result['Price'+str(date_range)+'_angle'] >= 500, 'Price'+str(date_range)+'_angle_Signal'] = 'P-Ultra'

        # -80 <= Slope < -30 : Weak
        result.loc[(result['Price'+str(date_range)+'_angle'] >= -80) & (result['Price'+str(date_range)+'_angle'] < -30), 'Price'+str(date_range)+'_angle_Signal'] = 'N-Weak'
        # -300 <= Slope < -80 : Strong
        result.loc[(result['Price'+str(date_range)+'_angle'] >= -300) & (result['Price'+str(date_range)+'_angle'] < -80), 'Price'+str(date_range)+'_angle_Signal'] = 'N-Strong'
        # -500 <= Slope < -300 : Super
        result.loc[(result['Price'+str(date_range)+'_angle'] >= -500) & (result['Price'+str(date_range)+'_angle'] < -300), 'Price'+str(date_range)+'_angle_Signal'] = 'N-Super'
        # 500 <= Slope : Ultra
        result.loc[result['Price'+str(date_range)+'_angle'] <= -500, 'Price'+str(date_range)+'_angle_Signal'] = 'N-Ultra'


        if inplace:
            self._update_inplace(result)

        return  self



    def ma_angle(self, column='Close', periods=[20], date_range=5, inplace=True):
        """
        Moving Average Angle calculation from given date range

        :param periods: given periods -> [list]
        :param date_range: date interval range [int]
        :param inplace: inplace or not -> True, False
        :return: Angel per day [Unit: degree/day]
        """
        from scipy.stats import linregress as lin

        if inplace:
            new_obj = self

        new_obj.ma(column=column, periods=periods)

        result = pd.DataFrame()

        for st in new_obj['Name'].unique():
            temp = new_obj[new_obj['Name'] == st]

            for per in periods:
                Res = []
                for k in range(len(temp)):
                    if k < date_range-1:
                        Res.append(np.nan)

                    else:
                        y = temp['MA_'+column+'_'+str(per)][k-date_range+1:k+1]
                        res = lin(range(date_range), y)
                        Res.append(str(res[0] / y.mean() * 100 * 100))

                try:
                    temp['MA_'+column+'_'+str(per)+'_angle'] = Res
                    temp['MA_'+column+'_'+str(per)+'_angle'] = temp['MA_'+column+'_'+str(per)+'_angle'].astype(float)
                except:
                    pass

            result = zipping(result, temp)

        if inplace:
            self._update_inplace(result)

        return  self


    def estrangement(self, column='Close', periods= [5,20], inplace= True):

        """
        Estrangement from given periods

        :param periods: iven periods -> [list]
        :param inplace: inplace or not -> True, False
        :return: Estrangement of given periods, [Unit: %]
        """
        if inplace:
            new_obj = self

        new_obj.ma(column=column, periods= periods)
        for per in periods:
            new_obj['EST_'+column+'_'+str(per)] = (new_obj[column] - new_obj['MA_'+column+'_'+str(per)]) / new_obj['MA_'+column+'_'+str(per)] *100
            new_obj['EST_'+column+'_'+str(per)] = new_obj['EST_'+column+'_'+str(per)]

        if inplace:
            self._update_inplace(new_obj)

        return  self


    def ma(self, column= 'Close', periods=[5,20], inplace=True):

        """
        Moving Average from given periods

        :param column: column to calculate -> [str]
        :param periods: given periods -> [list]
        :param inplace: inplace or not -> True, False
        :return: Moving Average
        """
        if inplace:
            new_obj = self

        result = pd.DataFrame()

        _num = 1
        for st in new_obj['Name'].unique():
            temp = new_obj[new_obj['Name'] == st]

            for per in periods:
                if ('MA_'+column+'_'+str(per)) not in new_obj.columns:
                    print(_num, st, 'SMA'+str(per))
                    temp['MA_'+column+'_'+str(per)] = pd.rolling_mean(temp[column], per)

            result = zipping(result, temp)

            _num += 1

        if inplace:
            self._update_inplace(result)

        return  self



    def ma_above(self, periods= [5,20], inplace= True):

        """
        Find Close Price is above ma of given periods

        :param periods: given periods -> [list]
        :param inplace: inplace or not -> True, False
        :return: above date is set by 'Up'
        """
        if inplace:
            new_obj = self

        new_obj.ma(periods= periods)

        for per in periods:
            new_obj.loc[new_obj['Close'] >  new_obj['MA'+str(per)], 'MA'+str(per)+'_above'] = 'Up'

        if inplace:
            self._update_inplace(new_obj)

        return  self



    def cross_finding(self, short_periods= 5, long_periods= 20, inplace= True):

        """
        Golden cross date finding from Long & Short periods

        :param short_periods: short ma criteria
        :param long_periods: long ma criteria
        :param inplace: inplace or not -> True, False
        :return: Golden & Dead cross date marked ['Golden', 'Dead']
        """
        if inplace:
            new_obj = self

        periods = []
        periods.append(short_periods)
        periods.append(long_periods)

        new_obj.ma(periods= periods)

        new_obj['MA Diff'] = new_obj['MA'+str(short_periods)] - new_obj['MA'+str(long_periods)]
        new_obj['Check'] = new_obj['MA Diff'] * new_obj['MA Diff'].shift(periods= 1)

        new_obj.loc[(new_obj['Check'] < 0) & (new_obj['MA Diff'] > 0), 'Cross'] = 'Golden'
        new_obj.loc[(new_obj['Check'] < 0) & (new_obj['MA Diff'] < 0), 'Cross'] = 'Dead'

        new_obj['MA Diff'] = (new_obj['MA Diff'] / new_obj['Close'] * 100).round(decimals= 1)

        new_obj.drop(labels= ['Check'], axis= 1, inplace= True)

        if inplace:
            self._update_inplace(new_obj)

        return  self


    def pct_change(self, inplace=True):

        """
        Percentage Change from given period

        :param inplace: inplace or not -> True, False
        :return: Percentage Change [Unit: %]
        """
        if inplace:
            new_obj = self

        result = pd.DataFrame

        for st in new_obj['Name'].unique():
            temp = new_obj[new_obj['Name'] == st]
            temp['PCT'] = (temp['Close'].pct_change() * 100).round(decimals= 1)

        result = zipping(result, temp)

        if inplace:
            self._update_inplace(result)

        return  self