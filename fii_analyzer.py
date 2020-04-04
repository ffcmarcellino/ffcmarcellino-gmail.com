import pandas as pd
from fii_crawler import *
import requests
import json
import datetime

class fiiAnalyzer:

    def __init__():
        pass

ticker_list = get_ticker_list()[:10]
crawler = fiiCrawler(ticker_list)

print(crawler.html_list[2])
