from marketsim.veusz_graph import Graph, showGraphs
from marketsim.scheduler import world
from marketsim.order_queue import OrderBook
from marketsim.trader import LiquidityProvider, FVTrader
from marketsim import Side
from marketsim.indicator import AssetPrice, BidPrice, AskPrice, OnEveryDt, EWMA

book_A = OrderBook(tickSize=0.01, label="A")

price_graph = Graph("Price")
spread_graph = Graph("Bid-Ask Spread")
 
assetPrice = AssetPrice(book_A)
price_graph.addTimeSerie(assetPrice)

spread_graph.addTimeSerie(BidPrice(book_A))
spread_graph.addTimeSerie(AskPrice(book_A))

ewma_0_15 = EWMA(assetPrice, alpha=0.15)
ewma_0_015 = EWMA(assetPrice, alpha=0.015)
ewma_0_065 = EWMA(assetPrice, alpha=0.065)

price_graph.addTimeSerie(OnEveryDt(1, ewma_0_15))
price_graph.addTimeSerie(OnEveryDt(1, ewma_0_015), {r'PlotLine/bezierJoin':True})
price_graph.addTimeSerie(OnEveryDt(1, ewma_0_065))

seller_A = LiquidityProvider(book_A, Side.Sell)
buyer_A = LiquidityProvider(book_A, Side.Buy)

world.workTill(500)

showGraphs("liquidity", [price_graph, spread_graph])

world.reset()