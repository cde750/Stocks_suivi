import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from tickers import get_sp500_tickers

# Récupération des tickers du S&P 500
sp500_tickers = get_sp500_tickers()

# Définition de la fonction pour créer le graphique d'un ticker
def plot_ticker(ticker, period="5y"):
    try:
        data = yf.download(ticker, period=period, interval="1wk")
        
        if data.empty:
            return None
        
        data.index = pd.to_datetime(data.index).tz_localize(None)
        data.columns = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
        data["MA30"] = data["Close"].rolling(window=30).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Prix de clôture"))
        fig.add_trace(go.Scatter(x=data.index, y=data["MA30"], mode="lines", name="Moyenne mobile 30 jours"))
        fig.update_layout(title=f"{ticker} - 5 ans glissants (weekly)", xaxis_title="Date", yaxis_title="Prix ($)")
        return fig
    except:
        return None
        
# Configuration de l'application Streamlit
st.set_page_config(page_title="Analyse des données boursières du S&P 500")
st.title("Analyse des données boursières du S&P 500")

# Affichage de la liste des tickers
st.subheader("Tickers du S&P 500")
st.write(", ".join(sp500_tickers[:30]))

# Affichage des graphiques pour les 30 premiers tickers
for ticker in sp500_tickers[:30]:
    st.subheader(f"Graphique pour {ticker}")

    fig = plot_ticker(ticker)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f"Données indisponibles pour le ticker {ticker}")