import csv
import sqlite3
import datetime as dt
from typing import NamedTuple
from data_validation import data_validation, assert_type


######### CREATE DATABASE CONNECTION ###########
con = sqlite3.connect('stock.db')
cur = con.cursor()

######### CREATE DATABASE TABLE###########
cur.execute("DROP TABLE IF EXISTS coinbase;")
cur.execute("CREATE TABLE coinbase (date, symbol, open_, high, low, \
             close, volume_btc, volume_usd )")

######### READ DATA FROM CSV ###########
class CryptoData(NamedTuple):
    date: dt.date
    symbol: str
    open_: float
    high: float
    low: float
    close: float
    volume_btc: float
    volume_usd: float
    
@assert_type
def read_crypto_data(filename):
    with open(filename, 'r') as infile:
        parsed_data = csv.DictReader(infile)
        for row in parsed_data:
            yield CryptoData(
            date = row['Date'],
            symbol = row['Symbol'],
            open_ = row['Open'],
            high = row['High'],
            low = row['Low'],
            close = row['Close'],
            volume_btc = row['Volume BTC'],
            volume_usd = row['Volume USD'])  
            
data = list(read_crypto_data('crypto_data.csv'))    

######### LOAD INTO DATABASE TABLE ###########
cur.executemany("INSERT INTO coinbase (date, symbol, open_, high, low, \
             close, volume_btc, volume_usd ) VALUES (?,?,?,?,?,?,?,?)", data )
con.commit()

######### PERFORM QUERY ###########
for row in con.execute('SELECT * FROM coinbase'):
    print(row)

min_price = 300
for row in con.execute('SELECT * FROM coinbase where open_ >=?',
(min_price,)):
    print(row)
        
    
        





    