import tushare as ts


class stockpool():

    def __init__(self):

        self._data = None

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

        return self.isvalid()

    def get_stock_sday(self, stock_id):

        """
        # get stock start date
        #
        # Parameters:
        #   stock_id : string
        #
        # return:
        #   start_date : string
        """

        try:
            start_date = self._data.ix[stock_id]['timeToMarket']
        except Exception as e:
            print(e)
        else:
            return str(start_date)

        return None

    def iterstock(self):

        for stock in self._data.index:
            if stock is not None:
                yield(stock)
