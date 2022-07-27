"""This package is designed to be ran afer the get_tickers package. It will 
create a dataframe from the ouput.csv and use the yfinance package to obtain sectors for
every stock with a ticker in the holdings. Finally, it will add these outputs as a column,
which it will save as a new csv. """

import yfinance as yf
import pandas as pd


df = pd.read_csv("Output.csv")

ticker_list = df['Ticker'].tolist()
sector_list=[]
for x in ticker_list:
    ticker = x
    ticker = str(ticker)
    ticker = yf.Ticker(ticker)
    sector = ticker.info['sector']
    sector_list.append(sector)
    
df['Sector'] = sector_list

df.to_csv("Output_Sector.csv")

