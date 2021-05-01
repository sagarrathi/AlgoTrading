from ibapi.client import EClient     ## For Connection
from ibapi.wrapper import EWrapper   ## For Translating all low level operations in high level python
from ibapi.contract import Contract  ## For contract as IBKR Trades around various exchanges

import threading
import time

import pandas as pd

class TradingApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self) #First self belongs to slef, other belongs to wrapper class
        self.data={}
        self.event=""
        
    def error(self, reqId, errorCode, errorString): # Copied from wrapper.py
        print("ReqId:",reqId, "Error:",errorCode,"Message:", errorString )
        
    def contractDetails(self, reqId, contractDetails):
        print("ReqId:", reqId,
             "Contract Details:", contractDetails)
        
    def headTimestamp(self, reqId, headTimestamp):
        print("ReqId:", reqId,"Earliest data available:",headTimestamp)

    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data[reqId]=[{"date":bar.date,
                               "open":bar.open,
                               "high":bar.high,
                               "low":bar.low,
                               "close":bar.close,
                               "volume":bar.volume}]
        else:
            self.data[reqId].append({"date":bar.date,
                                       "open":bar.open,
                                       "high":bar.high,
                                       "low":bar.low,
                                       "close":bar.close,
                                       "volume":bar.volume})
        
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print("ReqId:", reqId,"Historical Data Ended","from", start, "to", end)
        self.event.set()
        
    def historicalDataUpdate(self, reqId: int, bar):
        print("HistoricalDataUpdate. ReqId:", reqId, "BarData.", bar)

    
def contract_maker(symbol,sec_type="STK", exchange="NSE", currency="INR"):
    contract=Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.exchange =exchange
    contract.currency = currency
    return contract

def history_retriver(req_id,contract,app_obj,from_date,duration="2 D",bar_size="1 day", ):
    app_obj.reqHistoricalData(  reqId=req_id,
                            contract=contract,
                            endDateTime=from_date,
                            durationStr=duration,
                            barSizeSetting=bar_size,
                            whatToShow="TRADES",
                            useRTH=1,
                            formatDate=1,
                            keepUpToDate=False,
                            chartOptions=[]
                         )
def data_saver(df_dict, from_date, duration, bar_size):
    for ticker in df_dict:
        
        ###### Directory ##########
        dir_name= "./Data/"
        import os
        os.makedirs(dir_name, exist_ok=True)
        ############################
        
        ##### File Name ###########
        date_str=from_date.split(" ")[0]
        file_name=ticker+"_"+date_str+"_"+duration+"_"+bar_size+".csv"
        file_name=file_name.replace(" ", "")
        file_name=dir_name+file_name
        ############################
        
        df_dict[ticker].to_csv(file_name, index=False)
        print("Data saved to:",file_name)

        
def multi_historical_retriver(ticker_list,app_obj, from_date, duration,bar_size, event):
    df_dict={}
    for ticker in ticker_list:
        event.clear()
 
        ix=ticker_list.index(ticker)

        contract=contract_maker(ticker)
        time.sleep(1)  ## Wait for Client to make conecction and then pass this to to thread for reply
        history_retriver(ix, contract,app_obj,from_date, duration, bar_size)
        time.sleep(1)## Waiting for app.reqContract to finish before restarting kernel.
 
        event.wait()
 
        df_dict[ticker]=pd.DataFrame(app_obj.data[ix])
        time.sleep(1)
        
    data_saver(df_dict, from_date, duration, bar_size)
    

