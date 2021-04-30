import backtrader as bt
import backtrader.indicators as btind
import numpy as np
import datetime

class ReversalAction(bt.Strategy):
    
    
    
    params = (
        ('short_period',10),
        ('long_period',180),
        ('reversal_tol_factor',0.5),
        ('breakout_tol_factor',0.3),
        ('strike_at',"sr_price"),
        ('target_percentage',2),
        ('stop_percentage',0.5),
        ('closing_time',"15:10"),
        ('show_trades', False),
        ('execute_breakout',True),
        ('sr_levels',[]),
        ('order_time',"2:00"),
        ('order_at',"close_price"),
        ('show_trade_object',False),
        ('allow_shorting',False),
        ('cerebro', "")
        )
    
    def log(self,txt,dt=None):
        if dt is None:
            dt=self.datas[0].datetime.datetime()
        print(dt,txt)
        pass

    def tolerance(self,base_x,y,tolerance, dt=None):
        z=(base_x-y)/base_x
        z=np.abs(z)*100
        z=z<tolerance
        return z
        
        
    ############## Copied from Documenation #####################
    def notify_order(self, order):
        if self.params.show_trades:
            if order.status in [order.Submitted, order.Accepted]:
                # Buy/Sell order submitted/accepted to/by broker - Nothing to do
                return

            # Check if an order has been completed
            # Attention: broker could reject order if not enough cash
        
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log('BUY EXECUTED, %.2f' % order.executed.price)
                elif order.issell():
                    self.log('SELL EXECUTED, %.2f' % order.executed.price)

                self.bar_executed = len(self)

            elif order.status == order.Canceled:
                self.log('Order Canceled')
            elif order.status ==order.Margin: 
                    self.log('Order Margin')
            elif order.status ==order.Rejected: 
                    self.log('Order Rejected')
            
            # Write down: no pending order
            self.order = None
        #################################################################
    def notify_trade(self, trade):
        
        trade.historyon=True
        
        dt = self.data.datetime.datetime()
        if trade.isclosed:
            dt=self.datas[0].datetime.datetime()
            h1=["Date", 'Avg Price',  'Gross Profit',     'Net Profit',            'Len']
            r1=[dt,    trade.price,  round(trade.pnl,2),  round(trade.pnlcomm,2),  trade.barlen]
            table_values=[h1,r1]
            
            from tabulate import tabulate
            if self.params.show_trade_object:
                print(tabulate(table_values,))
            

    
    def __init__(self):
        
        self.start_datetime=self.datas[0].p.fromdate
        
        self.start_portfolio_value = self.params.cerebro.broker.getvalue()
        
        
        self.brought_today=False
        self.order =None
        
        self.sma_short = btind.EMA(self.datas[0], period=self.params.short_period)
        
        self.sma_long= btind.EMA(self.datas[0], period=self.params.long_period)
        
    #################  Printing Profit At end ################################
    def stop(self):   
        from tabulate import tabulate
        from babel.numbers import format_currency  as inr

        cerebro=self.params.cerebro

        start_portfolio_value=self.start_portfolio_value
        end_portfolio_value=int(cerebro.broker.getvalue())
        pnl=end_portfolio_value-self.start_portfolio_value
        
        start_portfolio_value  =   inr(start_portfolio_value, "INR", locale='en_IN')
        end_portfolio_value    =   inr(end_portfolio_value,   "INR", locale='en_IN')
        pnl                    =   inr(pnl,                   "INR", locale='en_IN')
        
        start_datetime=self.start_datetime
        end_datetime=self.datas[0].datetime.datetime()
        start_date=start_datetime.date()
        end_date=end_datetime.date()
        time_delta=end_datetime-self.start_datetime
        
        table_values= [
                        ["Date Time",start_date,            end_date,            time_delta.days],
                        ["Amount",   start_portfolio_value, end_portfolio_value, pnl],
                      ]        
        
        print (tabulate(table_values, 
                        headers=["Values","Started","Ended","Delta"],
                        tablefmt="grid"))

    ###############################################    
    
    
    def next(self):
        mid_bar_value= (self.datas[0].high[0] + self.datas[0].low[0] )/2
        open_p=self.datas[0].open[0]
        low_p=self.datas[0].low[0]
        high_p=self.datas[0].high[0]
        close_p=self.datas[0].close[0]
        
        open_p1=self.datas[0].open[-1]
        low_p1=self.datas[0].low[-1]
        high_p1=self.datas[0].high[-1]
        close_p1=self.datas[0].close[-1]
        
        cerebro=self.params.cerebro
        #################  Long Trend ################################
        if mid_bar_value>self.sma_long:
            long_trend="Up"
        else:
            long_trend="Down"
        ##############################################################
        
        
        #################  Short Trend ################################
        if mid_bar_value>self.sma_short:
            short_trend="Up"
        else:
            short_trend="Down"
        ##############################################################

        
        #################  SR Area ################################
        sr=self.params.sr_levels
        
        
        tol_factor=self.params.reversal_tol_factor
        if short_trend=="Up":
            z=self.tolerance(high_p,sr,tol_factor)
        else:
            z=self.tolerance(low_p,sr,tol_factor)
    
        z=np.matmul(z,np.transpose(sr))
    
        if z>0:
            area_of_value="In"
            area=z
        else:
            area_of_value="Out"
            area=""
        ###############################################################
        
        
        ################# Volume Support ################################
        if self.datas[0].volume[0]>self.datas[0].volume[-1]:
            volume_support="yes"
        else:
            volume_support="no"
        ###############################################################
        
        
        ################# Bar Lenght Support ################################
        bar_lenght_support=""
        if np.abs(open_p-close_p) > np.abs(open_p1-close_p1):
            bar_lenght_support="yes"
        else:
            bar_lenght_support="no"
        ###############################################################
        
        
        #################  Red Green Conversion ################################
        # Current Bar Color
        if close_p>open_p:
            bar_color="green"
        else:
            bar_color="red"
            
        # Previous Bar Color
        if close_p1>open_p1:
            previous_bar_color="green"
        else:
            previous_bar_color="red"
        
        trend_change=""
        if volume_support=="yes" and bar_lenght_support=="yes":
            if previous_bar_color=="green" and bar_color=="red":
                trend_change="green_to_red"
            elif previous_bar_color=="red" and bar_color=="green":
                trend_change="red_to_green"
            
            elif previous_bar_color=="green" and bar_color=="green":
                trend_change="green_to_green"
            elif previous_bar_color=="red" and bar_color=="red":
                trend_change="red_to_red"
                
        ########################################################################
        
        
        #################  To Buy/Sell/Wait ################################
        
        ############### Reversal
        order_signal=""
        if long_trend=="Up":
            if short_trend=="Down":
                if area_of_value=="In":
                    if trend_change=="red_to_green":
                        order_signal="Buy"
        
        if long_trend=="Down":
            if short_trend=="Up":
                if area_of_value=="In":
                    if trend_change=="green_to_red":
                        order_signal="Sell"
        
        ############### Breakout
        if self.params.execute_breakout:

            breakout_tol=self.params.breakout_tol_factor
            if long_trend=="Up":
                if short_trend=="Up":
                    if area_of_value=="In":
                        if ((close_p-area)/close_p)*100 >breakout_tol:
                            if trend_change=="green_to_green":
                                order_signal="Buy"                            

            if long_trend=="Down":
                if short_trend=="Down":
                    if area_of_value=="In":
                        if ((close_p-area)/close_p)*100 <breakout_tol:
                            if trend_change=="red_to_red":
                                order_signal="Sell"                            
        else:
            pass
        #################  Placing Bracket Order ################################
        strike_at=self.params.strike_at
        
        
        if strike_at =="mid_bar_price":
            strike_price=mid_bar_value
        elif strike_at=="sr_price":
            if area=="":
                strike_price=0
            else:
                strike_price=area
            
        ###### Target
        target_percentage=self.params.target_percentage
        buy_target=strike_price*(1+(target_percentage/100))
        sell_target=strike_price*(1-(target_percentage/100))
        
        ###### Stop Loss
        stop_percentage=self.params.stop_percentage
        buy_loss=strike_price*(1-(stop_percentage/100))
        sell_loss=strike_price*(1+(stop_percentage/100))
        
        
        ################### Placing Order ######################################
        order_hour=self.params.order_time.split(":")[0]
        order_hour=int(order_hour)
        order_minute=self.params.order_time.split(":")[1]
        order_minute=int(order_minute)
        
        
        
        if self.data.datetime.time() < datetime.time(order_hour,order_minute) \
            and not self.position.size\
            and (order_signal=="Buy" or order_signal=="Sell"):

            order_at=self.params.order_at
            if order_at=="close_price":
                order_price=close_p
            elif order_at=="mid_bar_price":
                order_price=mid_bar_value
            elif order_at=="sr_price":
                order_price=area
                
            cash=cerebro.broker.getvalue()
            cash=cash*(1-0.05)
            no_of_shares=int(cash/order_price)
            
            lots=int(no_of_shares/100)
            size=lots*100
            
            
            if order_signal=="Buy":
                if self.params.show_trades:
                    print("-------------------Buyed---------------:",size)
                self.order = self.buy_bracket(limitprice=buy_target, 
                                              price=order_price, 
                                              stopprice=buy_loss,
                                              size=size)
            if order_signal=="Sell" and self.params.allow_shorting:
                if self.params.show_trades:
                    print("-------------------Sold---------------",size)
                self.order = self.sell_bracket(limitprice=sell_target, 
                                               price=order_price, 
                                               stopprice=sell_loss,
                                               size=size)
        ########################################################################

        
        
        #################  Closing all Postion before 3:10 ################################
        close_hour=self.params.closing_time.split(":")[0]
        close_hour=int(close_hour)
        close_minute=self.params.closing_time.split(":")[1]
        close_minute=int(close_minute)
        
        if self.position.size != 0:
            if self.data.datetime.time() > datetime.time(close_hour,close_minute):
                    self.close(exectype=bt.Order.Market, size=self.position.size)
        ########################################################################
        
        
#         self.log("Close: "+str(close_p)+
#                 " Long Trend:"+long_trend+
#                 " Short Trend:"+short_trend+
#                 " Area :"+area_of_value+str(area)+
#                 " Trend Change: "+trend_change+
#                 " Order Signal: "+ order_signal)
    

