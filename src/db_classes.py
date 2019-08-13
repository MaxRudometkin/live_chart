from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Float

BASE = declarative_base()


class TradeHistoryLive(BASE):
    __tablename__ = 'trade_history_live'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    exchange = Column(String(20))
    market = Column(String(20))
    last = Column(Float)


    def __init__(self, date, exchange, market, last):
        self.date = date
        self.exchange = exchange
        self.market = market
        self.last = last




class Positions(BASE):

    __tablename__ = 'my_positions'

    id = Column(Integer, primary_key=True)
    exchange = Column(String(20))
    market = Column(String(20))
    open_date = Column(DateTime)
    side = Column(String(5))
    size = Column(Float)
    price = Column(Float)
    sl_price = Column(Float)
    tp_price = Column(Float)
    status = Column(String(10))
    close_date = Column(DateTime)
    close_price = Column(Float)
    pnl = Column(Float)


    def __init__(self,exchange, market, open_date,side,
                 size, price, sl_price, tp_price,status,
                 close_date,close_price, pnl):

        self.exchange = exchange
        self.market = market
        self.open_date = open_date
        self.side = side
        self.size = size
        self.price = price
        self.sl_price = sl_price
        self.tp_price = tp_price
        self.status = status
        self.close_date = close_date
        self.close_price = close_price
        self.pnl = pnl