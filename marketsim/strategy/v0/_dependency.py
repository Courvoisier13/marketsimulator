from marketsim import (parts, observable, types, meta, defs, _, ops,
                       Side, registry, orderbook, bind, order, mathutils)

from _wrap import wrapper2
from _fv import FundamentalValueBase

from marketsim.types import *

class _Dependency_Impl(FundamentalValueBase):
    
    def __init__(self):
        self._priceToDependOn = observable.MidPrice(self.bookToDependOn) 
        self._orderFactoryT = self.orderFactory
        FundamentalValueBase.__init__(self)

    def _fundamentalValue(self):
        return self._priceToDependOn() * self.factor \
            if self._priceToDependOn() is not None else None
    
    def _volume(self, side):
        oppositeQueue = self._trader.orderBook.queue(side.opposite)
        # should we send limit and cancel orders here?
        oppositeVolume = oppositeQueue.volumeWithPriceBetterThan(self._fundamentalValue())
        # we want to trade orders only with a good price
        return min(oppositeVolume, self.volumeDistr())
    
    @property
    def _eventGen(self):
        return self._priceToDependOn        

exec wrapper2("Dependency", 
             """ Dependent price strategy believes that the fair price of an asset *A* 
                 is completely correlated with price of another asset *B* and the following relation 
                 should be held: *PriceA* = *kPriceB*, where *k* is some factor. 
                 It may be considered as a variety of a fundamental value strategy 
                 with the exception that it is invoked every the time price of another
                 asset *B* changes. 
             
                 It has following parameters: 
                 
                 |orderFactory| 
                     order factory function (default: order.Market.T)
                 
                 |bookToDependOn| 
                     reference to order book for another asset used to evaluate fair price of our asset
                 
                 |factor| 
                     multiplier to obtain fair asset price from the reference asset price
                     
                 |volumeDistr| 
                     defines volumes of orders to create 
                     (default: exponential distribution with |lambda| = 1)
             """,
             [('bookToDependOn','None',                             'IOrderBook'),
              ('orderFactory',  'order.MarketFactory',              'Side -> Volume -> IOrder'),
              ('factor',        '1.',                               'positive'),
              ('volumeDistr',   'mathutils.rnd.expovariate(.1)',    '() -> Volume')], register=False)
