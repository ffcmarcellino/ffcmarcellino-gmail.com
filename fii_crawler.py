import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import json

def get_ticker_list():
    url = "https://www.fundsexplorer.com.br/funds/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    ticker_span_list = soup.find_all('span', class_ = "symbol")
    ticker_list = [span.get_text() for span in ticker_span_list]

    return ticker_list

class fiiBaseCrawler:

    def __init__(self, ticker):

        self.soup1 = BeautifulSoup(page1.content, 'html.parser')
        self.soup2 = BeautifulSoup(page2.content, 'html.parser')

    def get_name(self):
        name = self.soup1.find('section', id = "basic-infos").find_all('div', class_ = 'col-md-6 col-xs-12')[0].find_all('span', class_ = 'description')[0].get_text()
        return name.strip()

    def get_type(self):
        type = self.soup1.find('section', id = "basic-infos").find_all('div', class_ = 'col-md-6 col-xs-12')[1].find_all('span', class_ = 'description')[3].get_text()
        return type.strip()

    def get_mgmt_type(self):
        mgmt_type = self.soup1.find('section', id = "basic-infos").find_all('div', class_ = 'col-md-6 col-xs-12')[0].find_all('span', class_ = 'description')[5].get_text()
        return mgmt_type.strip()

    def get_p_vp(self):
        p_vp = self.soup1.find('section', id = "main-indicators").find_all('span', class_ = 'indicator-value')[6].get_text()
        return float(p_vp.strip().replace(",","."))

    def get_current_price(self):
        current_price = self.soup1.find('span', class_ = "price").get_text()
        try:
            return float(current_price.strip().replace("R$ ", "").replace(".","").replace(",", "."))
        except:
            return None

    def get_months(self):
        rows = self.soup2.find('table', id = "last-revenues--table").find_all('tr')[1:]
        months = [tr.find_all("td")[1].get_text()[3:] for tr in rows]
        return months

    def get_revenues(self):
        rows = self.soup2.find('table', id = "last-revenues--table").find_all('tr')[1:]
        revenues = [float(tr.find_all("td")[4].get_text().replace("R$ ", "").replace(",", ".")) for tr in rows]
        return revenues

    def get_all_info(self):
        return self.get_name(), self.get_type(), self.get_mgmt_type(), self.get_p_vp(), self.get_current_price(), self.get_months(), self.get_revenues()

class fiiCrawler(fiiBaseCrawler):

    def __init__(self, ticker_list):
        self.ticker_list = ticker_list
        res = requests.get('http://127.0.0.1:3000/get-fii-info', params={'ticker_list': ticker_list}).text
        with open('html.json', 'r', encoding='utf-8') as f:
            self.html_list = json.load(f)
        print(res)

    def get_all_values(self, ticker_list, fun):
        values = []

        for i, ticker in enumerate(ticker_list):
            fiiBaseCrawler.__init__(ticker)
            values.append(getattr(self, fun)())

        return values

    def get_fii_df(self, ticker_list, name_list):
        fii_infos = []

        for ticker in enumerate(ticker_list):
            fiiBaseCrawler.__init__(ticker)
            fii_info = [ticker]
            fii_info += self.get_all_info()
            fii_infos.append(fii_info)

        return pd.DataFrame(columns = ["Ticker", "Name", "Type", "Mgmt Type", "P/VP", "Current Price", "Month", "Revenue"], data = fii_infos)
