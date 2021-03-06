from marketsim import ops, types, event, Side, _

def correct_volume(x):
    return None if x is None or abs(x) < 1 else int(x)
    
def correct_price(x):
    return x
    
def correct_budget(x):
    return x
    
def correct_side(x):
    return x

# tmpl = """
# class %(input)s(ops.Observable[types.%(output)s]): 
#     
#     def __init__(self, %(ini)s):
#         ops.Observable[types.%(output)s].__init__(self)
#         %(assign)s
#             
#     def __call__(self):
#         side = correct_side(self.side())
#         if side is None:
#             return None
#         volume = correct_volume(self.volume())
#         if volume is None:
#             return None
#         
#         return (side, volume)
#                     
#     _properties = {
#         'side'     : types.IFunction[Side],
#         'volume'   : types.IFunction[float],
#     }
# """
# 
# def generate(kind, cls, alias, docstring, fields, ctx):
#     def process(tmpl, sep=", "):
#         return sep.join([tmpl % mapped(locals()) for (name, ini, typ) in fields])
#     
#     args = process("%(name)s = None")
#     ctor = process("self._%(name)s = %(name)s if %(name)s is not None else %(ini)s", "; ")
#     props= process("\'%(name)s\' : %(typ)s")
#     binds = process("ctx.%(name)s = self._%(name)s", "; ")
#     pdefs = "".join([prop % locals() for (name, _,_) in fields])
#     reg = "@registry.expose("+str(alias)+")" if alias is not None else ""
#     name = cls.__name__
#     #print (tmpl + pdefs + trailer) % locals()
#     exec (tmpl + pdefs + trailer) % locals() in ctx

def subscribe_if_observable(source, target):
    if isinstance(source, types.IEvent):
        event.subscribe(source, _(target).fire, target)

class SideBase(object): 
    
    def __init__(self, side):
        self.side = side
        subscribe_if_observable(side, self)
            
    def __call__(self):
        side = self.side()
        if side is None:
            return None
        
        return side
                    
    _properties = {
        'side'   : types.IFunction[Side],
    }
    
class PriceBase(object): 
    
    def __init__(self, price = ops.constant(100)):
        self.price = price
        subscribe_if_observable(price, self)
            
    def __call__(self):
        price = self.price()
        if price is None:
            return None
        
        return price
                    
    _properties = {
        'price'   : types.IFunction[float],
    }
    
        
class VolumeBase(object): 
    
    def __init__(self, volume = ops.constant(1)):
        self.volume = volume
        subscribe_if_observable(volume, self)
            
    def __call__(self):
        volume = self.volume()
        if volume is None:
            return None
        
        return volume
                    
    _properties = {
        'volume'   : types.IFunction[float],
    }

VolumeBase_ = VolumeBase

class VolumeBase(VolumeBase_):
    
    def __call__(self):
        x = VolumeBase_.__call__(self)
        return None if x is None or abs(x) < 1 else int(x)
    
Volume = VolumeBase


class SideVolume(ops.Observable[types.SideVolume], SideBase, VolumeBase): 
    
    def __init__(self, 
                 side = ops.constant(Side.Sell), 
                 volume = ops.constant(1.)):
        ops.Observable[types.SideVolume].__init__(self)
        SideBase.__init__(self, side)
        VolumeBase.__init__(self, volume)
            
    def __call__(self):
        side = SideBase.__call__(self)
        
        if side is None:
            return None
        
        volume = VolumeBase.__call__(self)
        
        if volume is None:
            return None
        
        return (side, volume) 

class SignedVolume(ops.Observable[types.SideVolume]): 
    
    def __init__(self, 
                 signedVolume = ops.constant(1.)):
        ops.Observable[types.SideVolume].__init__(self)
        self.signedVolume = signedVolume
        subscribe_if_observable(signedVolume, self)
            
    
            
    def __call__(self):
        signedVolume = correct_volume(self.signedVolume())
        if signedVolume is None:
            return None
        side = Side.Buy if signedVolume > 0 else Side.Sell
        return (side, abs(signedVolume))
                    
    _properties = {
        'signedVolume'   : types.IFunction[float],
    }

class SidePriceVolume(ops.Observable[types.SidePriceVolume]): 
    
    def __init__(self, 
                 side = ops.constant(Side.Sell), 
                 price = ops.constant(100), 
                 volume = ops.constant(1)):
        ops.Observable[types.SidePriceVolume].__init__(self)
        self.side = side 
        self.price = price 
        self.volume = volume
        subscribe_if_observable(side, self)
        subscribe_if_observable(price, self)
        subscribe_if_observable(volume, self)
            
    def __call__(self):
        side = correct_side(self.side())
        if side is None:
            return None
        price = correct_price(self.price())
        if price is None:
            return None
        volume = correct_volume(self.volume())
        if volume is None:
            return None
        
        return (side, price, volume)
                    
    _properties = {
        'side'     : types.IFunction[Side],
        'price'    : types.IFunction[float],
        'volume'   : types.IFunction[float],
    }


class SideBudget(ops.Observable[types.SideBudget]): 
    
    def __init__(self, 
                 side = ops.constant(Side.Sell), 
                 budget = ops.constant(200.)):
        ops.Observable[types.SideBudget].__init__(self)
        self.side = side 
        self.budget = budget
        subscribe_if_observable(side, self)
        subscribe_if_observable(budget, self)
            
    def __call__(self):
        side = correct_side(self.side())
        if side is None:
            return None
        budget = correct_budget(self.budget())
        if budget is None:
            return None
        
        return (side, budget)
                    
    _properties = {
        'side'     : types.IFunction[Side],
        'budget'   : types.IFunction[float],
    }

