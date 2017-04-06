import tushare as ts
import datetime as dt


class StockBase():

    def __init__(self):

        self._data = None
        self._getsource()

    def isvalid(self):

        """
        # check if the stockpool is valuable
        """

        return self._data is not None

    def update(self):

        """
        # update the stockpool
        """

        return self._getsource()

    def _getsource(self):

        """
        # download stock pool
        """

        self._data = ts.get_stock_basics()

        print("Message: stockbase updating finish.")

        return self.isvalid()

    def stock_date_iter(self, stock_id, start=None, end=None):

        """
        # iterate single stock duration
        #
        # Parameters:
        #   stock_id : string
        #   start : int | iterator start index, like a list
        #   end : int | iterator end index, like a list
        #
        # return:
        #   start_date : string
        """

        if start is not None and not isinstance(start, int): 
            print("ValueError: start or number should be integer.")
            return None

        if end is not None and not isinstance(end, int):
            print("ValueError: start or number should be integer.")
            return None

        print("Message: try to get %s date information." % stock_id)
        try:
            start_date = self._data.ix[stock_id]['timeToMarket']
        except Exception as e:
            print("ValueError: stock %s does not exist in stock pool." % stock_id)
            return None
        else:
            if start_date == 0: 
                return None
            start_date = dt.datetime.strptime(str(start_date), "%Y%m%d").date()
        end_date = dt.datetime.now().date()

        if end is not None:
            end_date = min(start_date + dt.timedelta(days=end), end_date)

        if start is not None:
            start_date += dt.timedelta(days=start)

        while start_date <= end_date:
            if start_date.isoweekday() < 6:  # weekday
                yield str(start_date)

            start_date += dt.timedelta(days=1)

    def stock_id_iter(self, start=None, end=None):

        """
        # iterate stock code list
        #
        # Parameters:
        #   start : int | iterator start index, like a list
        #   end : int | iterator end index, like a list
        #
        # return:
        #   stock_id | string
        """

        if start is not None and not isinstance(start, int): 
            print("ValueError: start or number should be integer.")
            return None

        if end is not None and not isinstance(end, int):
            print("ValueError: start or number should be integer.")
            return None

        numrange = slice(start, end)

        for stock in self._data.index[numrange]:
            if stock is not None:
                yield(stock)
