import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la page Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Récupérer le contenu HTML de la page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Trouver le tableau contenant les informations
table = soup.find('table', {'id': 'constituents'})

# Charger le tableau dans un DataFrame
df = pd.read_html(str(table))[0]

# Afficher les premières lignes
print(df.head())

# Récupérer la liste des tickers
tickers = df['Symbol'].tolist()
