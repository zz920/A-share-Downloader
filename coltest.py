import collector
from stockpool import stockbase

if __name__ == "__main__":
    tmp_sp = stockbase()

    cnt = 10
    if not tmp_sp.isvalid(): exit()

    for code in tmp_sp.iterstock():
        if cnt < 1: break
        startdate, enddate = collector.collect_date(code, stockpool=tmp_sp)
        print(startdate, enddate)
        result = collector.collect_detail(code, "2017-03-30")
        print(result)


