import pandas as pd

def get_cac40_tickers():
    url = "https://en.wikipedia.org/wiki/CAC_40"
    tables = pd.read_html(url)
    cac40_df = tables[4]  # On choisit la 4ème table (index 3) où se trouve la composition du CAC 40.
    tickers = cac40_df['Ticker'].tolist()
    return tickers

# Exemple d'utilisation
cac40_tickers = get_cac40_tickers()
print(cac40_tickers)
