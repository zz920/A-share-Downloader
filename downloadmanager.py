import datetime
import multiprocessing
import logging
import time
import os
import _pickle as pickle
from functools import partial
from pandas.core import frame

import collector
import configure as CONF

from stockpool import StockBase
from sqlconnector import SqlConnector
from stockmodel import get_stock_class


class DownloadManager():

    def __init__(self, max_proc_num=4, sql_engine_URL=None):

        self._stockpool = StockBase()
        self._processpool = multiprocessing.Pool(max_proc_num)

        # sql connector
        self._connector = SqlConnector(sql_engine_URL)

        # clean the pickle file
        self._pkl_list = self._load()
        os.remove(CONF.DATAFILENAME)

    def run(self):

        logging.info("The DownloadManager Start.")
        valid_cnt = 0

        while not self._stockpool.isvalid() and valid_cnt < 5:
            self._stockpool.update()
            valid_cnt += 1
            time.sleep(5)

        if not self._stockpool.isvalid():
            logging.error("RuntimeError: download stock pool runtime.")
            raise RuntimeError("stock pool establish runtime")

        def _tosql(data, model, stock, date):
            if data is None:
                self._save(stock, date)
                return
            if len(data) < 10:
                pass
            else:
                self._connector.push_frame(model,
                    collector.data_adapter(date, data))

        # redownload stock in pkl file
        if len(self._pkl_list):
            logging.info("Download stock in pkl file.")
            for code, date in self._pkl_list:
                _tosql(collector.collect_detail(code, date))

        for stock in self._stockpool.stock_id_iter(0, 3):

            logging.info("Establish table for stock %s, download processing will start soon." % stock)

            stock_table = get_stock_class(stock)
            self._connector.create_table(stock_table)

            for date in self._stockpool.stock_date_iter(stock):
                self._processpool.apply_async(
                    collector.collect_detail,
                    (stock, date),
                    callback=partial(_tosql, **{'model':stock_table, 'stock':stock, 'date':date})
                )

        self._processpool.close()
        self._processpool.join()

    def _save(self, code, date, filepath=CONF.DATAFILENAME):

        """
        # pickle stock (code, date) pair into file
        # the multiprocessing lock problem should be sloved later
        """

        try:
            with open(filepath, 'ab') as pklfile:
                pickle.dump((code, date), pklfile)
        except Exception as e:
            logging.error(e)
            return False
        return True

    def _load(self, filepath=CONF.DATAFILENAME):

        """
        # load pkl file to get target (stock, date) pairs
        """
        result = []
        try:
            with open(filepath, 'rb') as pklfile:
                while True:
                    try:
                        result.append(pickle.load(pklfile))
                    except EOFError:
                        break
        except Exception as e:
            logging.error(e)
        finally:
            return result

if __name__ == '__main__':
    start = datetime.datetime.now()
    stockdownload = DownloadManager(20, CONF.DB_CONNECTION)
    stockdownload.run()
    end = datetime.datetime.now()
    logging.info("Stock download finished in %ss" % str(end-start))
