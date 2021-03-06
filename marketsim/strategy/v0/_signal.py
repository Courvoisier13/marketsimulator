import marketsim
from marketsim.types import *
from marketsim import (parts, order, mathutils, types, meta, defs, _, ops,
                       registry, signal, bind, signal, ops, observable)
from _two_sides import TwoSides

from _wrap import wrapper2

class SignalBase(TwoSides):
    
    def _orderFunc(self):
        threshold = self.threshold
        value = self._signalFunc()
        side =  None if (value is None or abs(value) <= self.threshold) \
                else (Side.Buy if value > 0 else Side.Sell)
        return (side, (self._volume(side),)) if side else None

    
    def _volume(self, side):
        return self.volumeDistr()

class _Signal_Impl(SignalBase):

    @property
    def _eventGen(self):    
        return self.signal
    
    @property
    def _signalFunc(self): 
        return self.signal
    
exec wrapper2("Signal", 
             """ Signal strategy listens to some discrete signal
                 and when the signal becomes more than some threshold the strategy starts to buy. 
                 When the signal gets lower than -threshold the strategy starts to sell. 
                 
                 It has following parameters:

                 |signal| 
                      signal to be listened to (default: RandomWalk)
                      
                 |orderFactory| 
                     order factory function (default: order.Market.T)
                     
                 |threshold| 
                     threshold when the trader starts to act (default: 0.7)
                     
                 |volumeDistr| 
                     defines volumes of orders to create 
                     (default: exponential distribution with |lambda| = 1)
             """,
             [('signal',        'signal.RandomWalk()',          'IObservable[float]'),  
              ('threshold',     '0.7',                          'non_negative'),
              ('orderFactory',  'order.MarketFactory',          'Side -> Volume -> IOrder'),
              ('volumeDistr',   'mathutils.rnd.expovariate(1.)','() -> Volume')])
