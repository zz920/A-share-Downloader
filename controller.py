import datetime
import multiprocessing
import logging
import time
import _pickle as pickle
from functools import partial
from pandas.core import frame

import collector
import configure as CONF

from stockpool import StockBase
from sqlconnector import SqlConnector
from stockmodel import StockTradeRecord


class StockDownloader():

    def __init__(self, max_proc_num=4, sql_engine_URL=None):

        self._stockpool = StockBase()
        self._processpool = multiprocessing.Pool(max_proc_num)

        # process manager
        _manager = multiprocessing.Manager()
        self._queue = _manager.Queue()

        # sql connector
        self._connector = SqlConnector(sql_engine_URL)

        # clean the pickle file
        """
        try:
            with open(CONF.DATAFILENAME,'wb') as f:
                f.write('')
        except:
            pass
        """

    def run(self):

        valid_cnt = 0

        while not self._stockpool.isvalid() and valid_cnt < 5:
            self._stockpool.update()
            valid_cnt += 1
            time.sleep(5)

        if not self._stockpool.isvalid():
            logging.error("RuntimeError: download stock pool runtime.")
            raise RuntimeError("stock pool establish runtime")

        for stock in self._stockpool.stock_id_iter(400, 401):
            for date in self._stockpool.stock_date_iter(stock):
                    result = self._processpool.apply_async(
                        collector.collect_detail,
                        (stock, date)
                    )
                    result.get()
 
        self._processpool.close()
        self._processpool.join()

    def _step(self, stock_id=None, date=None):

        """
        # single step of downloading
        #
        # parameters:
        #   stock_id : string | stock id 
        #   date : string | date
        # return:
        #   status : Boolean | success status
        """

        data = collector.collect_detail(stock_id, date)
 
        # fail to get data file with collector
        if isinstance(data, tuple):
            #plock.acquire()
            if not self._save(*data):
                logging.error("data: %s @ %s did not saved." % (stock_id, date))
            #plock.release()
            return None

        # save data in the database
        if isinstance(data, frame.DataFrame):
            if len(data) < 10:
                return None

        return data

    def _sendtodb(self):

        """
        # send to database
        """
        logging.debug("Try to push %s@%s in to sql." % (stock_id, date))
        data['stock_id'] = stock_id
        data['time'] = data['time'].map(
            lambda x: datetime.datetime.strptime(date+x, "%Y-%m-%d%H:%M:%S")
        )
        data.drop('change', axis=1, inplace=True)

        self._connector.push_frame(StockTradeRecord, data.to_dict(orient='records'))
        

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
            return None
        return result

    def __getstate__(self):

        """
        # Problem: http://stackoverflow.com/questions/25382455/python-notimplementederror-pool-objects-cannot-be-passed-between-processes
        """

        self_dict = self.__dict__.copy()
        del self_dict['_processpool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)

if __name__ == '__main__':
    start = datetime.datetime.now()
    stockdownload = StockDownloader(10, CONF.DB_CONNECTION)
    stockdownload.run()
    end = datetime.datetime.now()

    logging.info("Stock download finished in %ss" % str(end-start))
