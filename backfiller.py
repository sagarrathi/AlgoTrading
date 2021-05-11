def backfill_now(port=7496, clientId=23, tickers=['TATAMOTOR'], duration="20 D", bar_size="5 mins"):
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
    app.connect(host='127.0.0.1', port=port, clientId=clientId) #port 4002 for ib gateway paper trading/7497 for TWS paper trading


    con_thread = threading.Thread(target=websocket_con, daemon=True)
    con_thread.start()
    time.sleep(1) # some latency added to ensure that the connection is established
    
    ##################################################

    ##########  From Datetime #############
    import datetime
    today_date=(datetime.datetime.today().strftime("%Y%m%d %H:%M:%S"))
    ########################################

    tickers=tickers
    duration=duration
    bar_size=bar_size
    ########## Historical Data ############
    multi_historical_retriver(ticker_list=tickers,
                            app_obj=app, 
                            from_date=today_date,
                            duration=duration,
                            bar_size=bar_size,
                            event=event
                            )


    ########################################

    # Old Csv to sql
    from csv_to_sql import sql_ingester
    import sqlalchemy

    data_dir="./Data"
    sql_obj = sqlalchemy.create_engine('postgresql://krh:krh@123@localhost:5432/krh')
    df=sql_ingester(data_dir, sql_obj, False)
    ####################################################################################################################
