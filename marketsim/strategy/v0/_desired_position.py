from marketsim import event, _, Side, order, types, observable, trader, registry, signal, ops
from marketsim.types import *
from .._basic import Strategy
from .._wrap import wrapper2

class _DesiredPosition_Impl(Strategy):
    
    def __init__(self):
        Strategy.__init__(self)
        event.subscribe(self.desiredPosition, _(self)._wakeUp, self)
        self._tradedVolume = observable.VolumeTraded()
        self._pendingVolume = observable.PendingVolume()
        
    _internals = ['_tradedVolume', '_pendingVolume']
        
    def _wakeUp(self, dummy):
        desired = self.desiredPosition()
        if desired is not None:
            desired = int(desired)
            actual = self._tradedVolume() + self._pendingVolume()
            gap = desired - actual
            side = Side.Buy if gap > 0 else (Side.Sell if gap < 0 else None)
            if side is not None:
                order = self.orderFactory(side)(abs(gap))
                self._send(order)
                        
exec  wrapper2("DesiredPosition", 
             """ Generic strategy that tries to keep trader's position equal to *desiredPosition*, 
             
                 Parameters:
                 
                     |desiredPosition|
                         Observable telling desired position for the trader
                         
                     |orderFactory|
                         order factory function (default: order.Limit.T)
                         
             """,
              [('desiredPosition',      'None',                'types.IObservable[float]'), 
               ('orderFactory',         'order.MarketFactory', 'Side -> Volume -> IOrder'),], 
               register=False)
                
