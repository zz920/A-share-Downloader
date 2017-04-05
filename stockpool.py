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

    def stock_date_iter(self, stock_id):

        """
        # iterate single stock duration
        #
        # Parameters:
        #   stock_id : string
        #
        # return:
        #   start_date : string
        """

        print("Message: try to get %s date information." % stock_id)
        try:
            start_date = self._data.ix[stock_id]['timeToMarket']
        except Exception as e:
            print("ValueError: stock %s does not exist in stock pool." % stock_id)
            return None
        else:
            if start_date == 0: return None
            start_date = dt.datetime.strptime(str(start_date), "%Y%m%d").date()
        end_date = dt.datetime.now().date()

        while start_date <= end_date:
            if start_date.isoweekday() < 6:  #weekday
                yield str(start_date)
            start_date += dt.timedelta(days=1)

    def stock_id_iter(self):

        """
        # iterate stock code list
        #
        # return:
        #   stock_id | string
        """

        for stock in self._data.index:
            if stock is not None:
                yield(stock)
