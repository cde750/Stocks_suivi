# tickers.py
import pandas as pd

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    sp500_df = tables[0]
    tickers = sp500_df['Symbol'].tolist()
    return tickers
