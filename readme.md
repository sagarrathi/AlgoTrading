# Price Action Algo Trading 
## Trading reversal and Breakouts


[![N|Solid](https://img.shields.io/badge/Powered%20By-Backtrader-lightgrey)](https://interactivebrokers.github.io/tws-api/introduction.html)  
__And:__
[![N|Solid](https://interactivebrokers.github.io/tws-api/nav_iblogo.png)](https://interactivebrokers.github.io/tws-api/introduction.html)

[![Backtest Status](https://img.shields.io/badge/Backtesting%20-Passed-brightgreen.svg)](/backtest.py) 
[![Live Status](https://img.shields.io/badge/Live%20-Failed-red.svg)](/live.py)
[![Release](https://img.shields.io/badge/Release-v1.0-blue)](/releases/latest.html)

This code is for various Quants and Geeks who like to algo trade. 

### Strategy:
We use following price action Strategy:
- Detetcing if price is near Support/Resistance.
- Reversal if Engulfing Patter is formed
- Breakout if Support or Resistance is penetrated.
- Confluance of Volume and Candle power is also taken into account

### ✨Magic Behind The Scene:✨
1. The code gets all the data and saves as csv file in Data directory.
2. The CSV data is ingested in Postgresql Database, it also updates the new data if found from step 1.
3. The data is loaded in Pandas dataFrame for passing into Backtrader cerebro (aka brain).
4. All analysis is done and a Tear Sheet is generated for the stock. 


## Features
1. You can use single line function to download as much data from IBKR for a stock or list of stocks. Just remember not to abuse the API or you can be banned by IBKR.
2.  The strtegy rely on Support and Resistance level provided by you.
3.  You can easly bring the drawdown as low as 2%

## Tech
Our code uses very few open source project to run :
- [Backtrader] - For Backtesting.
- [Postgresql] - For storing data.
- [TWS API]    - For Retriving data 



## Installation

Install the all the pip packages.

```sh
    pip activate <your_enviorenment_name>
    pip install backtrader
    pip install pandas numpy matplotlib==3.2.0 plotly psycopg2 seaborn scipy SQLAlchemy statsmodels tabulate tzlocal
```

We require [TWS API](https://interactivebrokers.github.io/) requires  to run.
Download IBAPI from following: (https://interactivebrokers.github.io/)
And open terminal anf type following:

```sh
    cd ./IBJts/source/pythonclient/
    pip activate <your_enviorenment_name>
    python setup.py install
```

Install Postgres and create database.
```sh
    sudo apt-get install postgresql pgadmin
    sudo su postgres 
    psql
    >create user krh with encrypted password 'krh@123';
    >create database krh;     
    >grant all privileges on database krh to krh;
    >\q;
```

## Running Program

**First Step:**
[**Click Here to Download this Repo**](https://github.com/sagarrathi/KRH/archive/refs/heads/main.zip)
**Second Step:** 
Open terminal and run:
```sh
    pip activate <your_enviorenment_name>
    python backtest.py 
```
**Third Step:** 
Change parameters in backtest.py at function "cerebro.addstrategy".
Go back to **Step 2.**

> Most algo Traders and quants have to optimize the paramters and thus have to re run thier code many times.
> Thus we recommed to use VS Code Ide as by single click you can run. This will eliminate Step 2.
> Just by single click you can keep optimizing code.


## Python Files and their Usage
| Data Related | Usage|
|-----------------------------------------------------------------|------------------------------------------------------------------------------------|
| [backfiller.py](/backfiller.py)| It is used to obatin data. Function "backfill_now" does all magic for you.|
| **Strategy Related** ||
| [strategy/ReversalAction.py](/strategy/ReversalAction.py)| This is where our startegy reversal action is made. Skim through it|
| [analyzer.py](/analyzer.py)| This where we can add/remove various parametrers to judge.ex sharpe ratio, yield   |
| **For Actual Running**|                                                                                    |
| [backtest.py](/backtest.py)| Final backtesting libary. You only have to run this.                               |
| [live.py](/live.py) | Final backtesting libary for live trading. You only have to run this for trading.  |
| **Tutorial:**||
| [Ingester_baby_steps.ipynb](/Ingester_baby_steps.ipynb)| How to make data ingesting library step by step by using TWS API|
| [Ingester.ipynb](/Ingester.ipynb) | Final Ingester file for creating library|
| [Backtester_Step_By_Step.ipynb](/Backtester_Step_By_Step.ipynb) | How to learn Backtesting step by step using Backtarder Platform |
| **Output:**||
| [TATAMOTOR.html](/TATAMOTOR.html) | Tear Sheet for Tatat Motors, which was our x during this whole time.  |
| **Helper Files** |                                                                                    |
| [broker_to_csv.py](/broker_to_csv.py)| Helper fucntions to backfill_now, do not edit unless required|
| [csv_to_sql.py](/csv_to_sql.py)| Helper fucntions to backfill_now, do not edit unless required|
| [test.py](/test.py) | Dummy file do as you wish with this  |

##### Valid Bar Sizes:
#
|Size||||||||
|--- |--- |--- |--- |--- |--- |--- |--- |
|1 secs|5 secs|10 secs|15 secs|30 secs||||
|1 min|2 mins|3 mins|5 mins|10 mins|15 mins|20 mins|30 mins|
|1 hour|2 hours|3 hours|4 hours|8 hours||||
|1 day||||||||
|1 week||||||||
|1 month||||||||

#### Valid Duration String units:
| Unit | Description  |
| --- | --- |
| S | Seconds  |
| D | Day  |
| W | Week  |
| M | Month  |
| Y | Year  |


## Copyright
Copyright 2021 Sagar Rathi
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](/LICENSE.txt)


