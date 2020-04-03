import pandas as pd
from fii_crawler import *
import requests
import json
import datetime

class fiiAnalyzer:

    def __init__():
        pass

crawler = fiiCrawler()
# pages = crawler.get_all_values(crawler.get_ticker_list()[:10], 'get_current_price')
# print(pages)

start = datetime.datetime.now()
res = requests.get('http://127.0.0.1:3000/get-fii-info', params={'ticker_list': crawler.get_ticker_list()[:98]}).text
end = datetime.datetime.now()
print(res)
print(end-start)
# html_list = json.loads(res)
# print(len(html_list))
