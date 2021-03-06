from marketsim import types, event, _, ops, registry

class Base(ops.Observable[float]):
    """ Observable that fires if underlying source value becomes greater previous maximum plus some epsilon
    """

    def __init__(self):
        ops.Observable[float].__init__(self)
        self.value = None

    def _subscribe(self):
        self.value = self.source()
        self._handler = _(self)._fire
        if self.value is not None:
            self._handler = self._predicate(self.value + self._sign*self.epsilon(), self._handler)
        self.source += self._handler

    def bind(self, ctx):
        self._subscribe()

    def __call__(self):
        return self.value

    def _fire(self, dummy):
        if self.source() is not None:
            self.source -= self._handler
            self._subscribe()
            self.fire(dummy)

    @property
    def attributes(self):
        return {}


class MaxEpsilon_Impl(Base):
    """ Observable that fires if underlying source value becomes greater previous maximum plus some epsilon
    """
    _sign = +1
    _predicate = event.GreaterThan

class MinEpsilon_Impl(Base):
    """ Observable that fires if underlying source value becomes less than previous minimum minus some epsilon
    """

    _sign = -1
    _predicate = event.LessThan

