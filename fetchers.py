import requests

import os
import streamlit as st
from dotenv import load_dotenv
import anthropic

load_dotenv()

try:
	ETHERSCAN_API_KEY = st.secrets["ETHERSCAN_API_KEY"]
except (KeyError, FileNotFoundError):
	ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

try: 
	CRYPTOPANIC_API_KEY = st.secrets["CRYPTOPANIC_API_KEY"]
except (KeyError, FileNotFoundError):
	CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY")

try:
	ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]
except (KeyError, FileNotFoundError):
	ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

cliente_claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def obtener_gas_fees():
	url = "https://api.etherscan.io/v2/api"
	params = {
		"chainid": 1,
		"module": "gastracker",
		"action":"gasoracle",
		"apikey": ETHERSCAN_API_KEY
	}
	
	respuesta = requests.get(url, params=params)
	datos = respuesta.json()
	
	gas = float(datos["result"]["ProposeGasPrice"])
	
	return gas


import requests

def obtener_precio_eth():

	url = "https://api.coingecko.com/api/v3/simple/price"
	params = {
		"ids": "ethereum",
		"vs_currencies": "usd",
		"include_24hr_change": "true",
		"include_market_cap": "true"
	}

	respuesta = requests.get(url, params=params)
	datos = respuesta.json()

	precio = datos["ethereum"]["usd"]
	cambio = datos["ethereum"]["usd_24h_change"]
	market_cap = datos["ethereum"]["usd_market_cap"]

	return precio, cambio, market_cap

def obtener_tvl():
	url = "https://api.llama.fi/v2/historicalChainTvl/Ethereum"
	respuesta = requests.get(url)
	datos = respuesta.json()
	ultimo = datos[-1]
	tvl = ultimo["tvl"]
	return tvl

def obtener_stablecoin_supply(): 
	url = "https://stablecoins.llama.fi/stablecoins"
	respuesta = requests.get(url, params={"includePrices": "false"})
	datos = respuesta.json()

	total = 0
	for activo in datos["peggedAssets"]:
		en_ethereum = activo.get("chainCirculating", {}).get("Ethereum")
		if en_ethereum:
			valor_usd = en_ethereum.get("current", {}).get("peggedUSD", 0)			
			total += valor_usd

	return total

def obtener_eth_staking():
	url = "https://api.etherscan.io/v2/api"
	contrato_deposito = "0x00000000219ab540356cBB839Cbe05303d7705Fa"
	params = {
		"chainid": 1,
		"module": "account",
		"action": "balance",
		"address": contrato_deposito,
		"apikey": ETHERSCAN_API_KEY
	}
	
	respuesta = requests.get(url, params=params)
	datos = respuesta.json()

	print("Respuesta cruda de staking:", datos)

	balance_wei = int(datos["result"])
	eth_staked = balance_wei / 1e18       # convertir de wei a ETH
		
	
	return eth_staked

def obtener_tx_count():
	url = "https://api.growthepie.com/v1/export/txcount.json"
	respuesta = requests.get(url)
	datos = respuesta.json()

	filas_ethereum = [fila for fila in datos if fila["origin_key"] == "ethereum"]

	mas_reciente = max(filas_ethereum, key=lambda fila: fila["date"])

	tx_count = mas_reciente["value"]
	return tx_count

def obtener_active_addresses():
	url = "https://api.growthepie.com/v1/export/daa.json"
	respuesta = requests.get(url)
	datos = respuesta.json()

	filas_ethereum = [fila for fila in datos if fila["origin_key"] == "ethereum"]

	mas_reciente = max(filas_ethereum, key=lambda fila: fila["date"])

	active_addresses = mas_reciente["value"]
	return active_addresses

if __name__ == "__main__":
	print("Active addresses:", obtener_active_addresses())

def obtener_noticias_eth():
	url = "https://cryptocurrency.cv/api/news"
	params = {
		"limit": 20,
		"category": "ethereum"
	}
	respuesta = requests.get(url, params=params)
	
	datos = respuesta.json()
	noticias = datos.get("articles", [])
	return noticias 

if __name__ == "__main__":
	noticias = obtener_noticias_eth()
	print(f"Se encontraron {len(noticias)} noticias")

def generar_analisis_evento(titulo, descripcion, precio_actual, cambio_24h, gas_actual):
	prompt = f"""Eres un analista financiero especializado en Ethereum, escribiendo para el canal "Revolución Financiera".

Noticia: {titulo}
Resumen: {descripcion}

Contexto actual del mercado:
- Precio ETH: ${precio_actual:,.2f} ({cambio_24h:+.2f}% en 24h)
- Gas fee: {gas_actual:.3f} Gwei

Escribe un análisis breve (máximo 3 oraciones) en español, explicando por qué esta noticia es relevante para alguien que sigue el mercado de Ethereum, conectándola con el contexto actual si aplica. Tono profesional pero accesible."""

	respuesta = cliente_claude.messages.create(
		model="claude-haiku-4-5-20251001",
		max_tokens=300,
		messages=[{"role": "user", "content": prompt}]
	)
	
	return respuesta.content[0].text
if __name__ == "__main__":
	analisis = generar_analisis_evento(
		titulo="Ethereum staking supera niveles récord",
		descripcion="El total de ETH en staking alcanzó nuevos máximos históricos.",
		precio_actual=2500.00,
		cambio_24h=3.5,
		gas_actual=0.05
	)
	print(analisis)

# NOTA: "Transaction volume (USD)" quedó fuera del dashboard.
# No existe una API gratuita directa para este dato a nivel Ethereum L1.
# La alternativa viable es Dune Analytics (requiere cuenta + escribir una
# consulta SQL personalizada en su plataforma) — pendiente para una futura
# iteración del proyecto.
