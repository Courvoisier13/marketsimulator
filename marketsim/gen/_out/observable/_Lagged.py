from marketsim import registry
from marketsim.gen._intrinsic.observable.lagged import Lagged_Impl
from marketsim import IObservable
@registry.expose(["Basic", "Lagged"])
class Lagged(Lagged_Impl):
    """ 
    """ 
    def __init__(self, source = None, timeframe = None):
        from marketsim.gen._out._const import const
        from marketsim import event
        from marketsim import types
        from marketsim import event
        from marketsim import types
        self.source = source if source is not None else const()
        self.timeframe = timeframe if timeframe is not None else 10.0
        Lagged_Impl.__init__(self)
        if isinstance(source, types.IEvent):
            event.subscribe(self.source, self.fire, self)
        if isinstance(timeframe, types.IEvent):
            event.subscribe(self.timeframe, self.fire, self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'source' : IObservable,
        'timeframe' : float
    }
    def __repr__(self):
        return "Lagged_{%(timeframe)s}(%(source)s)" % self.__dict__
    
