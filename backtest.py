import pandas as pd

import sqlalchemy
sql_obj = sqlalchemy.create_engine('postgresql://krh:krh@123@localhost:5432/krh')

df_1min = pd.read_sql_table('tatamotor_1min', sql_obj, parse_dates={'date': {'format': '%Y-%m-%d %H:%M:%S'}})
df_5mins = pd.read_sql_table('tatamotor_5mins', sql_obj, parse_dates={'date': {'format': '%Y-%m-%d %H:%M:%S'}})

df_time_frames=[df_5mins]
df_time_frames[0].head()
#############################################################



####### Manin ###############

import backtrader as bt

from strategy import ReversalAction
from analyzer import printTradeAnalysis, printSQN

import datetime
import numpy as np


if __name__=='__main__':
    ticker_name="TATAMOTOR-STK-NSE"
    
    cerebro=bt.Cerebro()

    
    #Add data    
    for df in df_time_frames:
        data=bt.feeds.PandasData(dataname=df,
                        datetime=0,
                        fromdate=datetime.datetime(2021, 2, 1),

                        )
        cerebro.adddata(data)

        
    #Set Cash
    cerebro.broker.setcash(160000)
    
    
    

    #Add stratedgy to Cerebro 
    sr_levels=np.array([339.01,324.11,319.38,312.96,304.37,299.17,295.17,293.48,291.24,283.31]) 
    cerebro.addstrategy(ReversalAction, 
                        short_period=50,
                        long_period=200,
                        sr_levels=sr_levels,
        
                        reversal_tol_factor=1.5,
                        breakout_tol_factor=.3,
                        
                        order_time="15:00",
                        closing_time="15:10",
                        
                        show_trades= False,
                        show_trade_object=False,
                        
                        strike_at="sr_price",
                        order_at="mid_bar_price",
                        
                        target_percentage=2,
                        stop_percentage=1.2,

                        execute_breakout=True,
                        allow_shorting=True,
                       
                       cerebro=cerebro)
    
    
    #Adding Anylizer
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
    
    # Adding Observer
    cerebro.addobserver(bt.observers.DrawDown, plot=True, subplot=False)
    

    
    #RUN Cerebro Engine
    strategies=cerebro.run()
    
    # Capture results
    firstStrat = strategies[0]
    
    # print the analyzers
    printTradeAnalysis(firstStrat.analyzers.ta.get_analysis())
    printSQN(firstStrat.analyzers.sqn.get_analysis())
    
    portfolio_stats = firstStrat.analyzers.getbyname('PyFolio')
    returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
    returns.index = returns.index.tz_convert(None)

    import quantstats
    report_name=ticker_name.split("-")[0]
    quantstats.reports.html(returns, output=str(report_name+'.html'), title=report_name)
