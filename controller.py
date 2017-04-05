from stockpool import StockBase
import multiprocessing
import collector
import time


class StockDownloader():

    def __init__(self, max_proc_num=4):

        self._stockpool = StockBase()
        self._processpool = multiprocessing.Pool(max_proc_num)

    def start(self):

        valid_cnt = 0

        while not self._stockpool.isvalid() and valid_cnt < 5:
            self._stockpool.update()
            valid_cnt += 1
            time.sleep(5)

        if not self._stockpool.isvalid():
            print("RuntimeError: download stock pool runtime, check your internet connection.")
            raise RuntimeError("stock pool establish runtime")

        func = collector.collect_detail
        result = []

        for stock in self._stockpool.stock_id_iter():
            for date in self._stockpool.stock_date_iter(stock):
                    result.append(
                        self._processpool.apply_async(
                            func, (stock, date))
                    )

        self._processpool.close()
        self._processpool.join()

        for res in result:
            print(res.get())
            break
        print(len(result))


if __name__ == '__main__':
    stockdownload = StockDownloader()
    stockdownload.start()
