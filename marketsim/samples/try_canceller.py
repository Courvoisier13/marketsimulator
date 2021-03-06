import sys
sys.path.append(r'../..')

from marketsim import (strategy, trader, orderbook, order, ops, Side, mathutils,
                       observable, veusz, registry, timeserie)

from common import expose

@expose("Canceller", __name__)
def Canceller(ctx):

    ctx.volumeStep = 15

    return [
        ctx.makeTrader_A(strategy.v0.LiquidityProviderSide(side = Side.Sell),
                         "LiquidityProvider-"),
        
        ctx.makeTrader_A(strategy.LiquidityProvider(),
                         "LiquidityProviderEx-"),
         
        ctx.makeTrader_A(strategy.v0.LiquidityProviderSide(side = Side.Buy),
                         "LiquidityProviderBuy"),
    
        ctx.makeTrader_A(  strategy.v0.LiquidityProviderSide(
                                side = Side.Sell,
                                orderFactoryT=order.WithExpiryFactory(
                                    expirationDistr=ops.constant(10))),
                           "LiquidityProviderWithExpiry"),
        
        ctx.makeTrader_A(   strategy.v0.FundamentalValue(
                                fundamentalValue = ops.constant(1000)), 
                            "fv_1000")
        ]