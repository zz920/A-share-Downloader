from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class StockTradeRecord(BaseModel):

    __tablename__ = 'traderecord'

    id = Column(Integer, primary_key=True)
    stock_id = Column(String(6))
    time = Column(DateTime)
    price = Column(Float)
    volume = Column(BigInteger)
    amount = Column(BigInteger)
    type = Column(String(4))
