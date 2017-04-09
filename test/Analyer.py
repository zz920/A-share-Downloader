import cProfile
from controller import StockDownloader


def test():
    stockdownload = StockDownloader(10, "postgresql://zhibowen:zhibowen@localhost:5432/stockdb")
    stockdownload.start()

if __name__ == '__main__':
    cProfile.run('test()', 'result')
