tickers=['TATAMOTOR']
bar_size="1 min"

# from backfiller import backfill_now
# backfill_now(port=7496, clientId=35, tickers=tickers, duration="20 D", bar_size=bar_size)


import sqlalchemy
sql_obj = sqlalchemy.create_engine('postgresql://krh:krh@123@localhost:5432/krh')

import pandas as pd
df_dict=[]
for ticker in tickers:
    sql_table_name=ticker.lower()+"_"+bar_size.replace(" ","")
    df = pd.read_sql_table(sql_table_name, sql_obj, parse_dates={'date': {'format': '%Y-%m-%d %H:%M:%S'}})
    df_dict.append(df)



import backtrader as bt
from strategy.ReversalAction import ReversalAction

import numpy as np
import datetime

if __name__=='__main__':

    #Creating Cerebro Obect########
    cerebro=bt.Cerebro()
    ###############################

    ticker_name="TATAMOTOR-STK-NSE"
    
    ######### Add data to cerebro############   
    
    # Data preparation
    back_data=bt.feeds.PandasData(dataname=df_dict[0],
                                  datetime=0,
                                  fromdate=datetime.datetime(2021, 2, 1)
                                  )

    data = bt.feeds.IBData(dataname=ticker_name,
                            backfill_from=back_data,
                            host='127.0.0.1', port=7496, clientId=35    
                            )
    
    cerebro.resampledata(data,timeframe=bt.TimeFrame.Minutes, 
                            compression=5,
                            takelate=True,
                            )
                        
    
    cerebro.adddata(data)
    ###################################################
    
    
    
    ######### Add stratedgy to Cerebro ###############
    sr_levels=np.array([339.01,324.11,319.38,312.96,304.37,299.17,295.17,293.48,291.24,283.31]) 
    cerebro.addstrategy(ReversalAction,
                        short_period=50,
                        long_period=200,
                        sr_levels=sr_levels,
        
                        reversal_tol_factor=.8,
                        breakout_tol_factor=.5,
                        
                        order_time="15:20",
                        closing_time="18:00",
                        
                        show_trades= False,
                        show_trade_object=False,
                        
                        strike_at="sr_price",
                        order_at="mid_bar_price",
                        
                        target_percentage=1.8,
                        stop_percentage=1.2,

                        execute_breakout=True,
                        allow_shorting=False,
                       
                        cerebro=cerebro,
                       )
    
    ##########################################

    ############# RUN Cerebro Engine####################
    cerebro.run()
    ##################################################
       
        