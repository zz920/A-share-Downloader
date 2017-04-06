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
    """

    try:
        data = ts.get_tick_data(code, date, retry_count, pause)
        if data is None:
            raise(ValueError("stock code or date invalid"))
        print("Message: success getting %s data in %s." % (code, date))

    except Exception as e:
        # Network error
        if isinstance(e, IOError):
            # deal with the no result case
            print("IOError: tushare get_tick_data function failed. info: %s" % e)
        elif isinstance(e, ValueError):
            # deal with the data format invalid case
            print("ValueError: stock code %s or date %s invalid." % (code, date))

        return None

    else:
        return data


