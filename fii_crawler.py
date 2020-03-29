import requests
from bs4 import BeautifulSoup
import pandas as pd

class fiiBaseCrawler:

    def __init__(self, ticker):
        page = requests.get("https://fiis.com.br/" + ticker.lower())
        self.soup = BeautifulSoup(page.content, 'html.parser')

    def get_fii_type(self):
        return self.soup.find('div', id = "informations--basic").find_all('div', class_ = 'row')[0].find_all('div', class_ = 'item')[1].find('span', class_ = 'value').get_text()

    def get_asset_value(self):
        asset_value = self.soup.find('div', id = "informations--indexes").find_all('div', class_ = 'item')[3].find('span', class_ = 'value').get_text()

        return float(asset_value.replace("R$", "").replace(".","").replace(",","."))

    def get_current_price(self):
        current_price = self.soup.find('div', id = "quotations--wrapper").find_all('div', class_ = 'row')[2].find('div', class_ = "item quotation").find('span', class_ = 'value').get_text()

        return float(current_price.replace(".","").replace(",", "."))

    def get_months(self):
        rows = self.soup.find('table', id = "last-revenues--table").find_all('tr')[1:]

        months = [tr.find_all("td")[1].get_text()[3:] for tr in rows]

        return months

    def get_revenues(self):
        rows = self.soup.find('table', id = "last-revenues--table").find_all('tr')[1:]

        revenues = [float(tr.find_all("td")[4].get_text().replace("R$ ", "").replace(",", ".")) for tr in rows]

        return revenues

    def get_all_info(self):
        return self.get_fii_type(), self.get_asset_value(), self.get_current_price(), self.get_months(), self.get_revenues()

class fiiCrawler():

    def __init__(self):
        page = requests.get("https://fiis.com.br/lista-de-fundos-imobiliarios/")
        self.soup = BeautifulSoup(page.content, 'html.parser')

    def get_ticker_list(self):
        ticker_span_list = self.soup.find_all('span', class_ = "ticker")
        ticker_list = [span.get_text() for span in ticker_span_list]

        return ticker_list

    def get_name_list(self):
        name_span_list = self.soup.find_all('span', class_ = "name")
        name_list = [span.get_text() for span in name_span_list]

        return name_list

    def get_fii_infos(self):
        ticker_list = self.get_ticker_list()
        name_list = self.get_name_list()
        fii_infos = []

        for i, ticker in enumerate(ticker_list):
            fii = fiiBaseCrawler(ticker)
            fii_info = [ticker, name_list[i]]
            fii_info += fii.get_all_info()
            fii_infos.append(fii_info)

        return pd.DataFrame(columns = ["Ticker", "Name", "Type", "Asset Value per Share", "Current Price", "Month", "Revenue"], data = fii_infos)

crawler = fiiCrawler()
print(crawler.get_fii_infos())
