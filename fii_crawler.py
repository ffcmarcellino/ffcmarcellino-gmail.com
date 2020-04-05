import requests
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

    def __init__(self, html1, html2):

        self.soup1 = BeautifulSoup(html1, 'html.parser')
        self.soup2 = BeautifulSoup(html2, 'html.parser')

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
        try:
            return float(p_vp.strip().replace(",","."))
        except:
            return None

    def get_current_price(self):
        current_price = self.soup1.find('span', class_ = "price").get_text()
        try:
            return float(current_price.strip().replace("R$ ", "").replace(".","").replace(",", "."))
        except:
            return None

    def get_months(self):
        rows = self.soup2.find('table', id = "last-revenues--table").find_all('tr')[1:]
        months = [tr.find_all("td")[1].get_text()[3:] for tr in rows] if len(rows) > 0 else None
        return months

    def get_revenues(self):
        rows = self.soup2.find('table', id = "last-revenues--table").find_all('tr')[1:]
        revenues = [float(tr.find_all("td")[4].get_text().replace("R$ ", "").replace(",", ".")) for tr in rows] if len(rows) > 0 else None
        return revenues

    def get_all_info(self):
        return self.get_name(), self.get_type(), self.get_mgmt_type(), self.get_p_vp(), self.get_current_price(), self.get_months(), self.get_revenues()

class fiiCrawler(fiiBaseCrawler):

    def __init__(self, ticker_list):
        self.ticker_list = ticker_list
        with open('html1.json', 'r', encoding='utf-8') as f:
            self.html1_dict = dict(json.load(f))
        with open('html2.json', 'r', encoding='utf-8') as f:
            self.html2_dict = dict(json.load(f))

    def get_all_values(self, fun):
        values = []

        for ticker in self.ticker_list:
            fiiBaseCrawler.__init__(self, self.html1_dict[ticker], self.html2_dict[ticker])
            values.append(getattr(self, fun)())

        return values

    def get_fii_df(self):
        fii_infos = []

        for ticker in self.ticker_list:
            fiiBaseCrawler.__init__(self, self.html1_dict[ticker], self.html2_dict[ticker])
            fii_info = [ticker]
            fii_info += self.get_all_info()
            fii_infos.append(fii_info)

        return pd.DataFrame(columns = ["Ticker", "Name", "Type", "Mgmt Type", "P/VP", "Current Price", "Month", "Revenue"], data = fii_infos)
