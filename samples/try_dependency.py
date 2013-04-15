import sys, pickle
sys.path.append(r'..')

from marketsim import strategy, orderbook, trader, scheduler, observable, veusz, mathutils
from common import run

def Dependency(graph, world, books):

    book_A = books['Asset A']
    book_B = books['Asset B']

    price_graph = graph("Price")
     
    assetPrice_A = observable.Price(book_A)
    assetPrice_B = observable.Price(book_B)

    avg = observable.avg
    
    price_graph += [assetPrice_A,
                    avg(assetPrice_A, alpha=0.15),
                    avg(assetPrice_A, alpha=0.015),
                    avg(assetPrice_A, alpha=0.65),
                    assetPrice_B,
                    avg(assetPrice_B, alpha=0.15),
                    avg(assetPrice_B, alpha=0.015),
                    avg(assetPrice_B, alpha=0.65)]
    
    liqVol = mathutils.product(mathutils.rnd.expovariate(.1), mathutils.constant(5))
    t_A = trader.SASM(book_A, strategy.LiquidityProvider(defaultValue=50., volumeDistr=liqVol))
    t_B = trader.SASM(book_B, strategy.LiquidityProvider(defaultValue=150., volumeDistr=liqVol))
    
    dep_AB = trader.SASM(book_A, strategy.Dependency(book_B, factor=2), "AB")
    dep_BA = trader.SASM(book_B, strategy.Dependency(book_A, factor=.5), "BA")
    
    eff_graph = graph("efficiency")
    eff_graph += [observable.Efficiency(dep_AB),
                  observable.Efficiency(dep_BA),
                  observable.PnL(dep_AB),
                  observable.PnL(dep_BA)]

    return [t_A, t_B, dep_AB, dep_BA], [price_graph, eff_graph]

if __name__ == '__main__':    
    run("dependency", Dependency)