import time
import os
import logging
import multiprocessing

import configure as CONF
from util import *
from interface import SQLManager
from model import StockBase, get_stock_class


class DownloadManager():

    def __init__(self, max_proc_num=4, sql_engine_URL=None):

        self._stockpool = StockBase()
        self._max_proc_num = max_proc_num

        _q = multiprocessing.Manager().Queue(2 * max_proc_num)
        self._sqlmanager = SQLManager(_q, sql_engine_URL)
        self._que = _q

        self._pkl_list = load_from_pkl(CONF.DATAFILENAME)
        remove_pkl(CONF.DATAFILENAME)

    def start(self):

        logging.info("The DownloadManager Start.")
        valid_cnt = 0

        while not self._stockpool.isvalid() and valid_cnt < 5:
            self._stockpool.update()
            valid_cnt += 1
            time.sleep(5)

        if not self._stockpool.isvalid():
            logging.error("RuntimeError: download stock pool runtime.")
            raise RuntimeError("stock pool establish runtime")

        self._sqlmanager.start()

        # insert single data
        '''
        if len(self._pkl_list):
            logging.info("Start downloading the stock data in pkl file.")
            for stock, date in self._pkl_list:
                data = collect_detail(stock, date)
        '''

        for stock in self._stockpool.stock_id_iter(100, 102):

            logging.info("Establish table for stock %s, download processing will start soon." % stock)

            stock_table = get_stock_class(stock)
            self._sqlmanager.create_table(stock_table)

            pool = multiprocessing.Pool(self._max_proc_num)

            logging.info("Stock %s start downloading." % stock)
            result = []
            for date in self._stockpool.stock_date_iter(stock):
                result.append(pool.apply_async(
                    _save,
                    (stock, date)
                ))

            # wait for all process end.
            for item in result:
                while not item.ready():
                    time.sleep(1)
 
            pool.close()
            pool.join()

            logging.info("Stock %s finished." % stock)
            filename = stock + ".csv"
            tablename = stock_table.__tablename__
            tmpfile = os.path.join(CONF.TMPFILEDIR, filename)

            self._que.put((tmpfile, tablename))

        # wait until sql copy finished.
        while self._sqlmanager.is_alive():
            self._que.put(0)  # STOP SIGNAL
            time.sleep(3)
        logging.info("Stock download finished.")


def _save(stock, date):
    data = collect_detail(stock, date, pause=1)
    if data is None:
        pfile = CONF.DATAFILENAME
        if not os.path.exists(pfile):
            os.mknod(pfile)
        append_to_pkl((stock, date), pfile)
        return
    if len(data) < 10:
        return
    data = data_adapter(date, data)

    filename = stock + ".csv"
    tmpfile = os.path.join(CONF.TMPFILEDIR, filename)
    save_to_csv(data, tmpfile)


if __name__ == '__main__':

    stockdownload = DownloadManager(50, CONF.DB_CONNECTION)
    stockdownload.start()
