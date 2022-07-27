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

