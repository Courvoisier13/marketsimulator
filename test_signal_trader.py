from marketsim import Side
from marketsim.scheduler import Scheduler
from marketsim.order import *
from marketsim.order_queue import *
from marketsim.trader import *
from marketsim import signal
from marketsim import strategy

world = Scheduler()

book = OrderBook(tickSize=.001)

signal = signal.RandomWalk(initialValue=-2, deltaDistr=(lambda: 1), intervalDistr=(lambda:1))

trader = strategy.Signal(SASM_Trader(book), signal, volumeDistr=(lambda:10))

book.process(LimitOrderSell(110,10))
book.process(LimitOrderSell(120,10))

book.process(LimitOrderBuy(80,10))
book.process(LimitOrderBuy(90,10))

assert book.bids.best.price == 90

world.workTill(1.5)

assert book.bids.best.price == 80
assert trader.PnL == 90*10

world.workTill(2.5)

assert book.bids.best.price == 80
assert book.asks.best.price == 110
assert trader.PnL == 90*10

world.workTill(3.5)

assert book.bids.best.price == 80
assert book.asks.best.price == 120
assert trader.PnL == 90*10 - 110*10

world.workTill(4.5)

assert book.bids.best.price == 80
assert book.asks.empty
assert trader.PnL == 90*10 - 110*10 - 120*10
