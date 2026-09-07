import requests

import os
from dotenv import load_dotenv

load_dotenv()
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

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

