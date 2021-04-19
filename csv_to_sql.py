import pandas as pd

def csv_to_pandas(csv_file_name, bar_size):
    df=pd.read_csv(csv_file_name)
    
    long_bars=["1day","1week", "1month"]
    if bar_size in long_bars:
        df["date"]=pd.to_datetime(df["date"],format='%Y%m%d')
    else:
        df["date"]=pd.to_datetime(df["date"],format='%Y%m%d  %H:%M:%S')
    
    df.set_index("date", inplace=True)
    return df

def csv_name_to_data(file_name):
    ####### To Extarct Info from CSV file
    csv_file_name=file_name.split("/")[2]
    ticker=csv_file_name.split("_")[0]
    bar_size=csv_file_name.split("_")[3].split(".")[0]
    tabel_name=ticker+"_"+bar_size
    tabel_name=tabel_name.lower()
    return  tabel_name, bar_size


def sql_ingester(data_dir, engine, overwrite=False):
    
    from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Float
    
    
    ######### Csv Part #####
    import glob
    csv_list=glob.glob(data_dir+"/*")
    ########################    
    
    ##### Sql Part #######
    for file_name in csv_list:

        #### Extracting Info #########
        table_name, bar_size=csv_name_to_data(file_name)
        df=csv_to_pandas(file_name, bar_size)
        ##################################

        
        meta = MetaData()
        tick_table = Table(
        table_name, meta, 
        Column('date', DateTime, primary_key = True), 
        Column('open', Float),
        Column('high', Float),
        Column('low', Float),
        Column('close', Float),
        Column('volume', Float),
      )
        if table_name in engine.table_names():
            print(table_name,":")
            if overwrite:
                print("Table exist, deleting this and creating new table.")
                tick_table.drop(engine)
                tick_table.create(engine)
                df.to_sql(table_name, engine, if_exists='append', chunksize=5000, method='multi')
                print("Done")
            else:
                print("Table exist, updating record.")
                old_df=pd.read_sql_table(table_name,engine, index_col="date")
                df=df[~df.index.isin(old_df.index)]
                df.to_sql(table_name, engine, if_exists='append', chunksize=5000, method='multi')
                print("Done")
        else:
            print("Table does not exist, creating one.")
            tick_table.create(engine)
            df.to_sql(table_name, engine, if_exists='append', chunksize=5000, method='multi')
            print("Done")
            
     
    return df
