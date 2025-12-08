from enum import Enum
from typing import Optional
import MetaTrader5 as mt5
from pydantic import BaseModel


class TimeFrame(int, Enum):
    TIMEFRAME_M1 = mt5.TIMEFRAME_M1
    TIMEFRAME_M2 = mt5.TIMEFRAME_M2
    TIMEFRAME_M3 = mt5.TIMEFRAME_M3
    TIMEFRAME_M4 = mt5.TIMEFRAME_M4
    TIMEFRAME_M5 = mt5.TIMEFRAME_M5
    TIMEFRAME_M6 = mt5.TIMEFRAME_M6
    TIMEFRAME_M10 = mt5.TIMEFRAME_M10
    TIMEFRAME_M12 = mt5.TIMEFRAME_M12
    TIMEFRAME_M15 = mt5.TIMEFRAME_M15
    TIMEFRAME_M20 = mt5.TIMEFRAME_M20
    TIMEFRAME_M30 = mt5.TIMEFRAME_M30
    TIMEFRAME_H1 = mt5.TIMEFRAME_H1
    TIMEFRAME_H2 = mt5.TIMEFRAME_H2
    TIMEFRAME_H3 = mt5.TIMEFRAME_H3
    TIMEFRAME_H4 = mt5.TIMEFRAME_H4
    TIMEFRAME_H6 = mt5.TIMEFRAME_H6
    TIMEFRAME_H8 = mt5.TIMEFRAME_H8
    TIMEFRAME_H12 = mt5.TIMEFRAME_H12
    TIMEFRAME_W1 = mt5.TIMEFRAME_W1
    TIMEFRAME_MN1 = mt5.TIMEFRAME_MN1


class OrderType(int, Enum):
    ORDER_TYPE_BUY = mt5.ORDER_TYPE_BUY
    ORDER_TYPE_SELL = mt5.ORDER_TYPE_SELL
    ORDER_TYPE_BUY_LIMIT = mt5.ORDER_TYPE_BUY_LIMIT
    ORDER_TYPE_SELL_LIMIT = mt5.ORDER_TYPE_SELL_LIMIT
    ORDER_TYPE_BUY_STOP = mt5.ORDER_TYPE_BUY_STOP
    ORDER_TYPE_SELL_STOP = mt5.ORDER_TYPE_SELL_STOP
    ORDER_TYPE_BUY_STOP_LIMIT = mt5.ORDER_TYPE_BUY_STOP_LIMIT
    ORDER_TYPE_SELL_STOP_LIMIT = mt5.ORDER_TYPE_SELL_STOP_LIMIT
    ORDER_TYPE_CLOSE_BY = mt5.ORDER_TYPE_CLOSE_BY


class OrderFillingType(int, Enum):
    ORDER_FILLING_FOK = mt5.ORDER_FILLING_FOK
    ORDER_FILLING_IOC = mt5.ORDER_FILLING_IOC
    ORDER_FILLING_RETURN = mt5.ORDER_FILLING_RETURN


class OrderTimeType(int, Enum):
    ORDER_TIME_GTC = mt5.ORDER_TIME_GTC
    ORDER_TIME_DAY = mt5.ORDER_TIME_DAY
    ORDER_TIME_SPECIFIED = mt5.ORDER_TIME_SPECIFIED
    ORDER_TIME_SPECIFIED_DAY = mt5.ORDER_TIME_SPECIFIED_DAY


class TradeRequestActions(int, Enum):
    TRADE_ACTION_DEAL = mt5.TRADE_ACTION_DEAL
    TRADE_ACTION_PENDING = mt5.TRADE_ACTION_PENDING
    TRADE_ACTION_SLTP = mt5.TRADE_ACTION_SLTP
    TRADE_ACTION_MODIFY = mt5.TRADE_ACTION_MODIFY
    TRADE_ACTION_REMOVE = mt5.TRADE_ACTION_REMOVE
    TRADE_ACTION_CLOSE_BY = mt5.TRADE_ACTION_CLOSE_BY

class OrderTypeFilling(int, Enum):
    ORDER_FILLING_FOK = mt5.ORDER_FILLING_FOK
    ORDER_FILLING_IOC = mt5.ORDER_FILLING_IOC
    ORDER_FILLING_RETURN = mt5.ORDER_FILLING_RETURN

class OrderTypeTime(int, Enum):
    ORDER_TIME_GTC = mt5.ORDER_TIME_GTC
    ORDER_TIME_DAY = mt5.ORDER_TIME_DAY
    ORDER_TIME_SPECIFIED = mt5.ORDER_TIME_SPECIFIED
    ORDER_TIME_SPECIFIED_DAY = mt5.ORDER_TIME_SPECIFIED_DAY

class OrderRequest(BaseModel):
    action: TradeRequestActions
    magic: Optional[int] = None
    order: Optional[int] = None
    symbol: str
    volume: float
    price: float = 0
    stoplimit: Optional[float] = None
    sl: float = 0
    tp: float = 0
    deviation: int = 0
    type: Optional[OrderType] = None
    type_filling: Optional[OrderTypeFilling] = None
    type_time: Optional[OrderTypeTime] = None
    expiration: Optional[int] = None
    comment: str = ""
    position: Optional[int] = None
    position_by: Optional[int] = None


class LoginRequest(BaseModel):
    account: int
    password: str
    server: str
