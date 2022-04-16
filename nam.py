
import csv
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
def crypto_currency_name(article_tags):
    s = []
    name = article_tags.find_all('span',class_='tw-hidden d-lg-inline font-normal text-3xs ml-2')
    for wr in name:
    #     print(wr.text.strip())
        s.append(wr.text.strip())
#     print(s)
    return s
def crypto_currency_price(article_tags):
    p = []
    name1 = article_tags.find_all('td',class_='td-price price text-right pl-0')
    for wr in name1:
    #     print(wr.text.strip())
        p.append(wr.find('span',class_='no-wrap').text.strip())
#     print(p)
    return p
def trading_valuation_in_a_day(article_tags):
    h = []
    name1 = article_tags.find_all('td',class_='td-liquidity_score lit text-right col-market')
    for wr in name1:
    #     print(wr.text.strip())
        h.append(wr.find('span',class_='no-wrap').text.strip())
#     print(h)
    return h
def scrape_crypto_currency(crypto_url):
    # crypto_url = 'https://www.coingecko.com/'
    url = []
    response = requests.get(crypto_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(crypto_url))
    doc = BeautifulSoup(response.text, 'html.parser')
    article_tags = doc.find('div', class_='coin-table table-responsive')
    currency_dict = {
        'name': crypto_currency_name(article_tags),
        'price': crypto_currency_price(article_tags),
        'tradding-value': trading_valuation_in_a_day(article_tags)
    }
    df = pd.DataFrame(currency_dict)

    return df
def scrape_crypto_currency_all_pages(crypto_url):
    # crypto_url = 'https://www.coingecko.com'
    df = scrape_crypto_currency(crypto_url)
    df.to_csv('crypto_currency.csv')
    i =0
    while True and i < 2:
        response = requests.get(crypto_url)
        doc = BeautifulSoup(response.text, 'html.parser')
       
        x = doc.find('li',class_='page-item next')
        print(x.find('a')['href'])
        crypto_url = 'https://www.coingecko.com' + x.find('a')['href']
        df = scrape_crypto_currency(crypto_url)
        # f = 'crypto_currency' + str(i) + '.csv'
        # df.to_csv(f)
        response = requests.get(crypto_url)
        doc = BeautifulSoup(response.text, 'html.parser')
        article_tags = doc.find('div', class_='coin-table table-responsive')
        i+=1
    return
scrape_crypto_currency_all_pages('https://www.coingecko.com')
file1 = "crypto_currency.csv"
file2 = "crypto_currency0.csv"
file3 = "crypto_currency1.csv"

print("Merging multiple CSV files...")

# merge
dataFrame = pd.concat(
   map(pd.read_csv, [file1, file2,file3]), ignore_index=True)
print(dataFrame.head())
dataFrame.to_csv('crypto_currencyfinal.csv')