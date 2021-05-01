import sqlalchemy
import pandas as pd

sql_obj = sqlalchemy.create_engine('postgresql://krh:krh@123@localhost:5432/krh')

df_1min = pd.read_sql_table('tatamotor_1min', sql_obj, parse_dates={'date': {'format': '%Y-%m-%d %H:%M:%S'}})
df_5mins = pd.read_sql_table('tatamotor_5mins', sql_obj, parse_dates={'date': {'format': '%Y-%m-%d %H:%M:%S'}})

df_time_frames=[df_5mins]
df_time_frames[0].head()
#############################################################



import numpy as np
import backtrader as bt
from strategy import ReversalAction
import datetime

if __name__=='__main__':

    #Creating Cerebro Obect########
    cerebro=bt.Cerebro()
    ###############################

    ticker_name="TATAMOTOR-STK-NSE"
    
    ######### Add data to cerebro############   
    ibstore = bt.stores.IBStore(host='127.0.0.1', port=7496, clientId=35)
    cerebro.broker = ibstore.getbroker()
    #################################################################
    
    # Data preparation
    back_data=bt.feeds.PandasData(dataname=df_time_frames[0],
                                  datetime=0,
                                  fromdate=datetime.datetime(2021, 2, 1))
    data = bt.feeds.IBData(dataname=ticker_name, backtfill_from=back_data)
    
    cerebro.adddata(data)
    ###################################################
    
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=5)
    
    
    ######### Add stratedgy to Cerebro ###############
    sr_levels=np.array([339.01,324.11,319.38,312.96,304.37,299.17,295.17,293.48,291.24,283.31]) 
    cerebro.addstrategy(ReversalAction, 
                        short_period=50,
                        long_period=200,
                        sr_levels=sr_levels,
        
                        reversal_tol_factor=.8,
                        breakout_tol_factor=.3,
                        
                        order_time="15:10",
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
    
    ##########################################

    ############# RUN Cerebro Engine####################
    cerebro.run()
    ##################################################
       
        