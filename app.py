import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from tickers2 import get_cac40_tickers

# Récupération des tickers du CAC 40 (au lieu du S&P 500)
sp500_tickers = get_cac40_tickers()

# Définition de la fonction pour créer le graphique d'un ticker avec une comparaison d'indice
def plot_ticker(ticker, period="5y", benchmark="^FCHI"):
    try:
        # Télécharger les données du ticker
        data = yf.download(ticker, period=period, interval="1wk",auto_adjust =True)
        data = data.xs(ticker, axis=1, level='Ticker')

        
        # Vérifier si les données sont présentes
        if data.empty:
            return None

        # Télécharger les données de l'indice de référence
        benchmark_data = yf.download(benchmark, period=period, interval="1wk")
        
        # Vérifier si les données de l'indice sont présentes
        if benchmark_data.empty:
            return None
        
        # Préparer les données du ticker
        data.index = pd.to_datetime(data.index).tz_localize(None)
        data.columns = ["Open", "High", "Low", "Close","Volume"]
        data["MA30"] = data["Close"].rolling(window=30).mean()
        
        # Préparer les données de l'indice de référence
        benchmark_data.index = pd.to_datetime(benchmark_data.index).tz_localize(None)
        benchmark_data.columns = ["Open", "High", "Low", "Close", "Volume"]

        # Calculer le ratio entre le ticker et l'indice de référence
        data["Ratio"] = data["Close"] / benchmark_data["Close"]

        # Créer le graphique avec Plotly
        fig = go.Figure()

        # Tracer le cours de clôture du ticker
        fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Prix de clôture"))

        # Tracer la moyenne mobile du ticker
        fig.add_trace(go.Scatter(x=data.index, y=data["MA30"], mode="lines", name="Moyenne mobile 30 jours"))

        # Tracer le ratio entre le ticker et l'indice de référence sur l'axe secondaire
        fig.add_trace(go.Scatter(x=data.index, y=data["Ratio"], mode="lines" , name=f"Ratio {ticker}/{benchmark}", yaxis="y2"))

        # Configurer les axes
        fig.update_layout(
            title=f"{ticker} - Comparaison avec {benchmark} (5 ans glissants, weekly)",
            xaxis_title="Date",
            yaxis_title="Prix ($)",
            yaxis2=dict(title="Ratio Ticker/Indice", overlaying="y", side="right"),
        )

        return fig
    except Exception as e:
        print(f"Erreur pour le ticker {ticker}: {e}")
        return None

# Configuration de l'application Streamlit
st.set_page_config(page_title="Analyse des données boursières avec comparaison d'indice")
st.title("Analyse des données boursières avec comparaison d'indice")

# Choisir l'indice de référence
benchmark = st.selectbox("Choisissez un indice de référence", ["^FCHI", "^STOXX50E", "^SPX"])

# Affichage de la liste des tickers
st.subheader("Tickers du CAC 40")
st.write(", ".join(sp500_tickers[:40]))

# Affichage des graphiques pour les premiers tickers
for ticker in sp500_tickers[:40]:  # Limité à 10 pour des raisons de performance
    st.subheader(f"Graphique pour {ticker} avec comparaison {benchmark}")

    fig = plot_ticker(ticker, benchmark=benchmark)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f"Données indisponibles pour le ticker {ticker}")
