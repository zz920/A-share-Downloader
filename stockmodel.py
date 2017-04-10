from sqlalchemy import MetaData, Table, Column
from sqlalchemy import String, Integer, DateTime, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class StockTradeRecord(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    date = Column(String(10))
    time = Column(String(8))
    price = Column(Float)
    volume = Column(BigInteger)
    amount = Column(BigInteger)
    type = Column(String(4))

StockBaseTable = declarative_base(cls=StockTradeRecord)

def get_stock_class(stock_id):

    """
    # return a dynamic stock class with table name equal to "stock_(stock_id)"
    """
    if isinstance(stock_id, str) and len(stock_id) == 6:
        clsname = "stock_" + stock_id
        return type(clsname, (StockBaseTable,), {})
