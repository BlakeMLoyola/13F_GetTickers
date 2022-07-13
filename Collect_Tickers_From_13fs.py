""" this program was designed to collect tickers from CUSIPS using a fidelity
search engine. It will not be able to collect tickers from all 13F entries given
that CUSIPS and public stocks change a lot. It works best on recent 13F filings
but is also useful to get started on for older filings."""

import os
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import requests
import time


""" In order to run the program, 13fs must first be stored within a CSV file,
and the CUSIP Column must be called "CUSIP." See "Example_13F.csv" as a guide
for how I structured my CSV""""

files = pd.read_csv("ENTER_NAME.csv")
files = pd.DataFrame(files)


cusip_nums = set()
for file in files:
    cusip_nums = files.CUSIP
    
#Creating Ticker Dictionary
ticker_dic = {c:"" for c in cusip_nums}

#Running all cusips within ticker dictionary through the fidelity engine
for c in list(ticker_dic.keys()):
    url = "http://quotes.fidelity.com/mmnet/SymLookup.phtml?reqforlookup=REQUESTFORLOOKUP&productid=mmnet&isLoggedIn=mmnet&rows=50&for=stock&by=cusip&criteria="+c+"&submit=Search"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    ticker_elem = soup.find('tr', attrs={"bgcolor":"#666666"})
    ticker = ""
    try:
        ticker = ticker_elem.next_sibling.next_sibling.find('a').text
        ticker_dic[c] = ticker
    except:
        pass

    time.sleep(1)
    
# Mapping to dataframe
files['Ticker'] = files['CUSIP'].map(ticker_dic)

# Saving it to CSV
files.to_csv("Output.csv")
