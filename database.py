import sqlite3

def crear_tabla():
	conexion = sqlite3.connect("eth_dashboard.db")
	cursor = conexion.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS precios_eth (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			precio_usd REAL,
			cambio_24h REAL,
			fecha TEXT,
			market_cap REAL
			
		)
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS gas_fees(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			gas_gwei REAL,
			fecha TEXT

		)
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS defillama_metrics(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			tvl_usd REAL,
			stablecoin_supply_usd REAL,
			fecha TEXT
		)
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS staking_metrics(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			eth_staked REAL,
			fecha TEXT
		)
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS network_activity(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			tx_count REAL,
			active_addresses REAL,
			fecha TEXT
		)
	""")

	conexion.commit()
	conexion.close()

def guardar_precio(precio, cambio, marketcap, fecha):
	conexion = sqlite3.connect("eth_dashboard.db")
	cursor = conexion.cursor()
	cursor.execute(
		"INSERT INTO precios_eth (precio_usd, cambio_24h, market_cap, fecha) VALUES (?, ?, ?, ?)", (precio, cambio, marketcap, fecha)
	)
	conexion.commit()
	conexion.close()


def guardar_gas(gas, fecha):
	conexion = sqlite3.connect("eth_dashboard.db")
	cursor = conexion.cursor()
	cursor.execute(
		"INSERT INTO gas_fees (gas_gwei, fecha) VALUES (?, ?)", (gas, fecha)
	)
	conexion.commit()
	conexion.close()

def guardar_defillama(tvl, stablecoins, fecha):
	conexion = sqlite3.connect("eth_dashboard.db")
	cursor = conexion.cursor()
	cursor.execute(
		"INSERT INTO defillama_metrics (tvl_usd, stablecoin_supply_usd, fecha) VALUES (?, ?, ?)", (tvl, stablecoins, fecha)
	)
	conexion.commit()
	conexion.close()

def guardar_staking(stake, fecha):
	conexion = sqlite3.connect("eth_dashboard.db")
	cursor = conexion.cursor()
	cursor.execute(
		"INSERT INTO staking_metrics (eth_staked, fecha) VALUES (?, ?)", (stake, fecha)
	)
	conexion.commit()
	conexion.close()

def guardar_network_activity(tx, addresses, fecha):
	conexion = sqlite3.connect("eth_dashboard.db")
	cursor = conexion.cursor()
	cursor.execute(
		"INSERT INTO network_activity (tx_count, active_addresses, fecha) VALUES (?, ?, ?)", (tx, addresses, fecha)
	)
	conexion.commit()
	conexion.close()

import pandas as pd

def cargar_ultimo(tabla):
	conexion = sqlite3.connect("eth_dashboard.db")
	query = f"SELECT * FROM {tabla} ORDER BY fecha DESC LIMIT 1"
	df = pd.read_sql_query(query, conexion)
	conexion.close()
	if df.empty:
		return None
	return df.iloc[0]

def cargar_historial(tabla, limite=100):
	conexion = sqlite3.connect("eth_dashboard.db")
	query = f"SELECT * FROM {tabla} ORDER BY fecha ASC LIMIT {limite}"
	df = pd.read_sql_query(query, conexion)
	conexion.close()
	return df