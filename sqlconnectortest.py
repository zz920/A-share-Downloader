import sqlconnector as sql
import stockmodel as sm
import datetime as dt

if __name__ == '__main__':

    conn = sql.SqlConnector("postgresql://zhibowen:zhibowen@localhost:5432/stockdb")
    tmp = sm.StockTradeRecord(
        stock_id = "123456",
        trade_time = dt.datetime.now(),
        price = 10.9,
        volume = 100,
        amount = 10000,
        trade_type = "sell"
    )

    #conn.push_object(tmp)

    a = {
        'stock_id' : "123456", 
        'trade_time' : dt.datetime.now(),
        'price' : 10.9,
        'volume' : 100,
        'amount' : 10000,
        'trade_type' : "sell"
    }

    b = [a]*10000
    start = dt.datetime.now()
    conn.push_frame(sm.StockTradeRecord, b)
    end = dt.datetime.now()
    print(end - start)
