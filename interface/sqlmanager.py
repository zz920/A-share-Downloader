import os
import logging

from multiprocessing import Process
from interface.sqlconnector import SqlConnector
from interface.config import SIGNAL


class SQLManager(Process):

    def __init__(self, q, sql_engine_URL=None):

        self._que = q
        self._connector = SqlConnector(sql_engine_URL)
        super(SQLManager, self).__init__()

    def run(self):

        while True:
            signal = self._que.get()

            if signal is SIGNAL.STOP:
                break

            csvfile, table = signal

            if os.path.exists(csvfile):
                status = self._connector.copy_csvfile(table, csvfile)

            try:
                if status:
                    os.remove(csvfile)
            except:
                logging.error("FileError: can't remove file located in %s" % csvfile)

    def create_table(self, model):
        self._connector.create_table(model)
