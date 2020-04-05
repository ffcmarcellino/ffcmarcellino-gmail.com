import pandas as pd
from fii_crawler import *
import requests

class fiiAnalyzer:

    def __init__(fii_df):
        self.fii_df = fii_df

    

ticker_list = get_ticker_list() # INTERSECÇÃO ENTRE WEBSITES !!

for ticker in ["BTGM11", "FCAS11", "NCHB11B", "FFCI11", "OULG11B", "RDES11", ]:
    ticker_list.remove(ticker)

# requests.get('http://127.0.0.1:3000/get-fii-info', params={'ticker_list': ticker_list}).text
crawler = fiiCrawler(ticker_list)
print(crawler.get_fii_df())
