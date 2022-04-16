import csv
import requests
import pandas as pd
import xml.etree.ElementTree as ET
  
import requests
from bs4 import BeautifulSoup
def scrape_crypto_currency_all_pages(crypto_url):
    # crypto_url = 'https://www.coingecko.com'
    i =0
    urls = []
    while True and i < 1:
        response = requests.get(crypto_url)
        doc = BeautifulSoup(response.text, 'html.parser')
        urls.append(crypto_url)
        x = doc.find('li',class_='page-item next')
        print(x.find('a')['href'])
        crypto_url = 'https://www.coingecko.com' + x.find('a')['href']
        urls.append(crypto_url)
        response = requests.get(crypto_url)
        doc = BeautifulSoup(response.text, 'html.parser')
        article_tags = doc.find('div', class_='coin-table table-responsive')
        i+=1
    return urls

# uls = scrape_crypto_currency_all_pages(crypto_url)
def get_full_name(crypto_url):
    f = []
    make_url = []
    urls = scrape_crypto_currency_all_pages(crypto_url)
    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('Failed to load page {}'.format(crypto_url))
        doc = BeautifulSoup(response.text, 'html.parser')
        article_tags = doc.find('div', class_='coin-table table-responsive')
        name2 = article_tags.find_all('div',class_='tw-flex tw-items-center')
        for wr in name2:
            f.append(wr.find('a',class_='tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between')['href'])
        #     return f
    print(len(f))
    base_url = 'https://www.coingecko.com'
    for na in f:
        url = base_url + na
        make_url.append(url)
    return make_url

def supply(crypto_url):
    urls = get_full_name(crypto_url)
    circulating_supply = []
    total_supply = []
    currency_name = []
    market_cap = []
#     max_supply = []
   
    for url in urls:
        response = requests.get(url)
        doc = BeautifulSoup(response.text, 'html.parser')
        bond = doc.find('div',class_='tw-flex tw-text-gray-900 dark:tw-text-white tw-mt-2 tw-items-center')
        currency_name.append(bond.text.strip())
        martket_tags = doc.find('div', class_='tailwind-reset tw-col-span-2 lg:tw-col-span-1')
        for t in martket_tags.find_all('div'):
            if 'Market Cap' in t.find('span',class_='tw-text-gray-500 dark:tw-text-white dark:tw-text-opacity-60').text.strip():
                cs = t.find('span',class_='tw-text-gray-900 dark:tw-text-white tw-font-medium')
                market_cap.append(cs.text.strip())
                break
        
        totl_tags = doc.find('div', class_='tailwind-reset lg:tw-pl-4 tw-col-span-2 lg:tw-col-span-1')
        for t in totl_tags.find_all('div'):
            if 'Circulating Supply' in t.find('span',class_='tw-text-gray-500 dark:tw-text-white dark:tw-text-opacity-60').text.strip():
                cs = t.find('span',class_='tw-text-gray-900 dark:tw-text-white tw-font-medium tw-mr-1')
                circulating_supply.append(cs.text.strip())
            if 'Total Supply' in t.find('span',class_='tw-text-gray-500 dark:tw-text-white dark:tw-text-opacity-60').text.strip():
                cs = t.find('span',class_='tw-text-gray-900 dark:tw-text-white tw-font-medium tw-mr-1')
                total_supply.append(cs.text.strip())
    currency_supply = {
        'Currency Name':currency_name,
        'Circulating-Supply': circulating_supply,
        'Total-Supply': total_supply,
        'Market Cap':market_cap
    }
    df = pd.DataFrame(currency_supply)
    market_cap = list(set(market_cap))
    print(len(circulating_supply),'+++',len(total_supply),len(market_cap),len(currency_name))
    df.to_csv('crypto_supply.csv')
    # print(currency_supply)
    return
crypto_url = 'https://www.coingecko.com'
supply(crypto_url)