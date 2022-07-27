# 13F_GetTickers
T
This program is designed to get tickers using Fidelity's CUSIP Search engine. 
First, the User must enter a CIK for the fund they desire. Next, the program will pull the last two quarterly 13fs from EDGAR, and create
csvs titled last_report and previous_report. It will then concatanate the two files, and use the fidelity search engine to also obtain tickers
from the associated CUSIPS. 
  *note that CUSIPS change often, and a holding may not return a ticker if the code as changed.
