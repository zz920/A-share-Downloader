import logging
import tushare as ts
from datetime import datetime


def collect_detail(code=None, date=None, retry_count=4, pause=2):

    """
    # collect history trade detail
    #
    # Parameters:
    #  code : string  |stock id
    #  date : string  |target date
    #  retry_count : int  | retry times
    #  pause : int  | single request fail pause time
    #
    # return:
    #  data : DataFrame | all trade detail
    #           attr: time, price, change, volume, amount, type
    #         or tuple  | fail to get data, return the code and date
    """

    try:
        data = ts.get_tick_data(code, date, retry_count, pause)
        if data is None:
            raise(ValueError("stock code or date invalid"))
        logging.debug("success getting %s data in %s." % (code, date))

    except Exception as e:
        # Network error
        if isinstance(e, IOError):
            # deal with the no result case
            logging.error("IOError: tushare get_tick_data function failed. info: %s" % e)
            return (code, date)

        elif isinstance(e, ValueError):
            # deal with the data format invalid case
            logging.error("ValueError: stock code %s or date %s invalid." % (code, date))

        return None

    else:
        return data
