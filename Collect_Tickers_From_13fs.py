from unicodedata import name
import pandas as pd
import requests
import re
import csv
import lxml
from bs4 import BeautifulSoup
import time
import yfinance as yf

sec_url = 'https://www.sec.gov'


# Defining request
def get_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'HOST': 'www.sec.gov',
    }
    return requests.get(url, headers=headers)


#URL for EDGAR
def create_url(cik):
    return 'https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany&type=13F-HR'.format(cik)


# Input of CIK by User
def get_user_input():
    cik = input("Enter 10-digit CIK number: ")
    return cik
requested_cik = get_user_input()

def get_quarters():
    years = int(input("Please enter the number of years you would like to pull ('2' would pull previous 8 quarters):"))
    quarter = 4
    quarters = int(years*quarter)
    return quarters


                  


#Scraping the company report
def scrap_company_report(requested_cik):
    # Find mutual fund by CIK number on EDGAR
    response = get_request(create_url(requested_cik))
    soup = BeautifulSoup(response.text, "html.parser")
    tags = soup.findAll('a', id="documentsbutton")

    last_report = (sec_url + tags[0]['href'])
    previous_report = (sec_url + tags[1]['href'])

    
    scrap_report_by_url(last_report, "last_report")
    scrap_report_by_url(previous_report, "previous_report")
    
  
        


def scrap_report_by_url(url, filename):
    response_two = get_request(url)
    soup_two = BeautifulSoup(response_two.text, "html.parser")
    tags_two = soup_two.findAll('a', attrs={'href': re.compile('xml')})
    xml_url = tags_two[3].get('href')

    response_xml = get_request(sec_url + xml_url)
    soup_xml = BeautifulSoup(response_xml.content, "lxml")
    xml_to_csv(soup_xml, filename)

#Creating CSV out of XML
def xml_to_csv(soup_xml, name):

    columns = [
        "Name of Issuer",
        "CUSIP",
        "Value (x$1000)",
        "Shares",
        "Investment Discretion",
        "Voting Sole / Shared / None"
    ]
    issuers = soup_xml.body.findAll(re.compile('nameofissuer'))
    cusips = soup_xml.body.findAll(re.compile('cusip'))
    values = soup_xml.body.findAll(re.compile('value'))
    sshprnamts = soup_xml.body.findAll('sshprnamt')
    sshprnamttypes = soup_xml.body.findAll(re.compile('sshprnamttype'))
    investmentdiscretions = soup_xml.body.findAll(re.compile('investmentdiscretion'))
    soles = soup_xml.body.findAll(re.compile('sole'))
    shareds = soup_xml.body.findAll(re.compile('shared'))
    nones = soup_xml.body.findAll(re.compile('none'))

    df = pd.DataFrame(columns= columns)

    for issuer, cusip, value, sshprnamt, sshprnamttype, investmentdiscretion, sole, shared, none in zip(issuers, cusips, values, sshprnamts, sshprnamttypes, investmentdiscretions, soles, shareds, nones):
        row = {
            "Name of Issuer": issuer.text,
            "CUSIP": cusip.text,
            "Value (x$1000)": value.text,
            "Shares": f"{sshprnamt.text} {sshprnamttype.text}",
            "Investment Discretion": investmentdiscretion.text,
            "Voting Sole / Shared / None": f"{sole.text} / {shared.text} / {none.text}"
        }
        df = df.append(row, ignore_index=True)

    df.to_csv(f"{name}.csv")


    




scrap_company_report(requested_cik)


#Generating CSV of last and previous report
df1 = pd.DataFrame(pd.read_csv("last_report.csv"))
df2 = pd.DataFrame(pd.read_csv("previous_report.csv"))

#Concat the two Dfs
dfs = [df1,df2]
result = pd.concat(dfs)




#Using fidelity search engine to return tickers for holdings, some may not return ticker if CUSIP has changed
cusip_nums = set()
for row in dfs:
    cusip_nums = result.CUSIP

ticker_dic = {c:"" for c in cusip_nums}
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
    

#mapping results
result['Ticker'] = result['CUSIP'].map(ticker_dic)
    
  


result.to_csv("Output.csv")

    
# Mapping to dataframe
files['Ticker'] = files['CUSIP'].map(ticker_dic)

# Saving it to CSV
files.to_csv("Output.csv")
