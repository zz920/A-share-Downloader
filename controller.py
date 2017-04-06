import multiprocessing
import time
import datetime
from functools import partial

from pandas.core import frame

import collector

from stockpool import StockBase
from sqlconnector import SqlConnector
from stockmodel import StockTradeRecord 


class StockDownloader():

    def __init__(self, max_proc_num=4, sql_engine_URL=None):

        self._stockpool = StockBase()
        self._processpool = multiprocessing.Pool(max_proc_num)
        self._connector = SqlConnector(sql_engine_URL)

    def start(self):

        valid_cnt = 0

        while not self._stockpool.isvalid() and valid_cnt < 5:
            self._stockpool.update()
            valid_cnt += 1
            time.sleep(5)

        if not self._stockpool.isvalid():
            print("RuntimeError: download stock pool runtime.")
            raise RuntimeError("stock pool establish runtime")

        func = collector.collect_detail
        result = []

        for stock in self._stockpool.stock_id_iter(203, 205):
            for date in self._stockpool.stock_date_iter(stock):
                    result.append(
                        self._processpool.apply_async(
                            func,
                            (stock, date),
                            callback=partial(self.send, **{'stock_id':stock, 'date' : date})
                        )
                    )

        self._processpool.close()
        self._processpool.join()

    def send(self, result, stock_id=None, date=None):

        """
        # send download result to target
        """

        if len(result) < 10:
            return None

        #trans result format
        if isinstance(result, frame.DataFrame):
            print("Try to push %s@%s in to sql." % (stock_id, date))
            result['stock_id'] = stock_id
            result['time'] = result['time'].map(
                lambda x : datetime.datetime.strptime(date+x, "%Y-%m-%d%H:%M:%S")
            )
            result.drop('change', axis=1, inplace=True)

            self._connector.push_frame(StockTradeRecord, result.to_dict(orient='records'))



if __name__ == '__main__':
    start = datetime.datetime.now()
    stockdownload = StockDownloader(20, "postgresql://zhibowen:zhibowen@localhost:5432/stockdb")
    stockdownload.start()
    end = datetime.datetime.now()

    print("Stock download finished in %ss" % str(end-start))
