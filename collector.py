import tushare as ts
from datetime import datetime

import stockpool as sp


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
    """

    try:
        data = ts.get_tick_data(code, date, retry_count, pause)
        if data is None:
            raise(ValueError("stock code or date invalid"))

    except Exception as e:
        # Network error
        if isinstance(e, IOError):
            # deal with the no result case
            pass
        elif isinstance(e, ValueError):
            # deal with the data format invalid case
            pass
        print(e)
        return None

    else:
        return data


def collect_date(code=None, end=None):

    """
    # get single stock duration
    #
    # Parameters:
    #   code : string  |stock id
    #
    # return:
    #   (s_day, e_day) : (datetime.date, datetime.date)  | duration
    """

    if code is None or end is None or len(end) != 8:
        raise (ValueError("stock code or date invalid"))

    datetext = sp.get_stock_sday(code)
    if datetext is None or len(datetext) != 8:
        raise (ValueError("stock code or date invalid"))

    def date_func(s):
        return datetime.strptime(s, "%Y%m%d").date()

    s_day = date_func(datetext)
    e_day = datetime.now().date() if end is None else date_func(end)

    return (s_day, e_day)
