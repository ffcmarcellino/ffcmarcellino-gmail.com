import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd

class fiiBaseCrawler:

    def __init__(self, ticker):
        page1 = requests.get('https://www.fundsexplorer.com.br/funds/' + ticker.lower())
        self.soup1 = BeautifulSoup(page1.content, 'html.parser')
        page2 = requests.get('https://fiis.com.br/' + ticker.lower())
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

class fiiCrawler():

    def __init__(self):
        self.url1 = "https://www.fundsexplorer.com.br/funds/"
        self.url2 = "https://fiis.com.br/"
        page = requests.get(self.url1)
        self.soup = BeautifulSoup(page.content, 'html.parser')

    async def get_page(self, url):
        return requests.get(url).content

    async def get_list_pages(self, ticker_list):
        list_pages1 = []
        list_pages2 = []
        for ticker in ticker_list:
            t1 = self.loop.create_task(self.get_page(self.url1 + ticker.lower()))
            t2 = self.loop.create_task(self.get_page(self.url2 + ticker.lower()))
            list_pages1.append(t1)
            list_pages2.append(t2)
        t = datetime.datetime.now()
        await asyncio.wait(list_pages1 + list_pages2)
        print(datetime.datetime.now() - t)
        return zip([page.result() for page in list_pages1], [page.result() for page in list_pages2])

    def get_all_pages(self, ticker_list):
        self.loop = asyncio.get_event_loop()
        pages = self.loop.run_until_complete(self.get_list_pages(ticker_list))
        self.loop.close()
        return pages

    def get_ticker_list(self):
        ticker_span_list = self.soup.find_all('span', class_ = "symbol")
        ticker_list = [span.get_text() for span in ticker_span_list]

        return ticker_list

    def get_all_values(self, ticker_list, fun):
        values = []

        for i, ticker in enumerate(ticker_list):
            print(ticker)
            fii = fiiBaseCrawler(ticker)
            values.append(getattr(fii, fun)())

        return values

    def get_fii_infos(self, ticker_list, name_list):
        fii_infos = []

        for ticker in enumerate(ticker_list):
            fii = fiiBaseCrawler(ticker)
            fii_info = [ticker]
            fii_info += fii.get_all_info()
            fii_infos.append(fii_info)

        return pd.DataFrame(columns = ["Ticker", "Name", "Type", "Mgmt Type", "P/VP", "Current Price", "Month", "Revenue"], data = fii_infos)
