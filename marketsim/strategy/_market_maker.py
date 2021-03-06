from marketsim import (trader, orderbook, event, _, Side, order, types, mathutils, 
                       ops, observable, registry, combine, parts)

from marketsim.types import *

from _generic import Generic
from _market_data import BreaksAtChanges
from _array import Array
import _wrap

const = ops.constant
from marketsim.gen._out.observable.orderbook._Queue import Queue

class MarketMaker(types.ISingleAssetStrategy):
    
    def getImpl(self):
        volumeTraded = observable.VolumeTraded(trader.SingleProxy())

        return Array([
                Generic(
                    order.factory.Iceberg(
                        ops.constant(10),
                        order.factory.FloatingPrice(
                            BreaksAtChanges(
                                observable.OnEveryDt(
                                    0.9,
                                    parts.price.SafeSidePrice(Queue(orderbook.OfTrader(), ops.constant(side)), ops.constant(100 + sign))\
                                        / ops.Exp(ops.Atan(volumeTraded) / 1000)
                            )),
                            order._limit.Price_Factory(
                                side = const(side),
                                volume = const(self.volume * 1000000)))),
                event.After(ops.constant(0)))\
                    for side, sign in {Side.Buy : -1, Side.Sell : 1}.iteritems()
            ])

_wrap.strategy(MarketMaker, ['Market maker'],
             """

             |volume|
                Volume of Buy/Sell orders. Should be large compared to the volumes of other traders.
             """,
              [ ('volume', '20.', 'Volume') ], globals())