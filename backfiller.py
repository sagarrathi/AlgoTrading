from broker_to_csv import TradingApp, multi_historical_retriver
import pandas as pd

import threading
import time
##########  Starting App as Thread #############
def websocket_con():
    app.run()
    

event = threading.Event() 

app = TradingApp()
app.event=event
app.connect(host='127.0.0.1', port=7496, clientId=23) #port 4002 for ib gateway paper trading/7497 for TWS paper trading


con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1) # some latency added to ensure that the connection is established
 
##################################################


##########  From Datetime #############
import datetime
today_date=(datetime.datetime.today().strftime("%Y%m%d %H:%M:%S"))
########################################


########## Historical Data ############
tickers=['TATAMOTOR']
multi_historical_retriver(ticker_list=tickers,
                         app_obj=app, 
                         from_date=today_date,
                         duration="20 D",
                         bar_size="5 mins",
                         event=event
                         )


########################################


def kernel_restarter():
    from IPython.display import display_html
    display_html("<script>Jupyter.notebook.kernel.restart()</script>",raw=True)
kernel_restarter()
