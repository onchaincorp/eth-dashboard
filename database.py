import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

try:
	import streamlit as st
	DATABASE_URL = st.secrets["DATABASE_URL"]
except (KeyError, FileNotFoundError, ImportError):
	DATABASE_URL = os.getenv("DATABASE_URL")

def get_conexion():
	return psycopg2.connect(DATABASE_URL)

def crear_tabla():
	conexion = get_conexion()
	cursor = conexion.cursor()

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS precios_eth (
			id SERIAL PRIMARY KEY,
			precio_usd REAL,
			cambio_24h REAL,
			fecha TEXT,
			market_cap REAL
		)
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS gas_fees (
			id SERIAL PRIMARY KEY,
			gas_gwei REAL,
			fecha TEXT
		)
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS defillama_metrics (
			id SERIAL PRIMARY KEY,
			tvl_usd REAL,
			stablecoin_supply_usd REAL,
			fecha TEXT
		)
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS staking_metrics (
			id SERIAL PRIMARY KEY,
			eth_staked REAL,
			fecha TEXT
		)
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS network_activity (
			id SERIAL PRIMARY KEY,
			tx_count REAL,
			active_addresses REAL,
			fecha TEXT
		)
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS eventos_mercado (
			id SERIAL PRIMARY KEY,
			fecha_noticia TEXT,
			titulo TEXT,
			fuente TEXT,
			url TEXT UNIQUE,
			analisis_ia TEXT,
			fecha_creacion TEXT
		)
	""")
	
	conexion.commit()
	cursor.close()
	conexion.close()

def guardar_precio(precio, cambio, marketcap, fecha):
	conexion = get_conexion()
	cursor = conexion.cursor()
	cursor.execute(
		"INSERT INTO precios_eth (precio_usd, cambio_24h, market_cap, fecha) VALUES (%s, %s, %s, %s)",
		(precio, cambio, marketcap, fecha)
	)
	conexion.commit()
	cursor.close()
	conexion.close()

def guardar_gas(gas, fecha):
	conexion = get_conexion()
	cursor = conexion.cursor()
	cursor.execute(
		"INSERT INTO gas_fees (gas_gwei, fecha) VALUES (%s, %s)",
		(gas, fecha)
	)
	conexion.commit()
	cursor.close()
	conexion.close()

def guardar_defillama(tvl, stablecoins, fecha):
	conexion = get_conexion()
	cursor = conexion.cursor()
	cursor.execute(
		"INSERT INTO defillama_metrics (tvl_usd, stablecoin_supply_usd, fecha) VALUES (%s, %s, %s)",
		(tvl, stablecoins, fecha)
	)
	conexion.commit()
	cursor.close()
	conexion.close()

def guardar_staking(stake, fecha):
	conexion = get_conexion()
	cursor = conexion.cursor()
	cursor.execute(
		"INSERT INTO staking_metrics (eth_staked, fecha) VALUES (%s, %s)",
		(stake, fecha)
	)
	conexion.commit()
	cursor.close()
	conexion.close()

def guardar_network_activity(tx, addresses, fecha):
	conexion = get_conexion()
	cursor = conexion.cursor()
	cursor.execute(
		"INSERT INTO network_activity (tx_count, active_addresses, fecha) VALUES (%s, %s, %s)",
		(tx, addresses, fecha)
	)
	conexion.commit()
	cursor.close()
	conexion.close()

def guardar_evento(fecha_noticia, titulo, fuente, url, analisis_ia, fecha_creacion):
	conexion = get_conexion()
	cursor = conexion.cursor()
	try:
		cursor.execute(
			"INSERT INTO eventos_mercado (fecha_noticia, titulo, fuente, url, analisis_ia, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s)",
			(fecha_noticia, titulo, fuente, url, analisis_ia, fecha_creacion)
		)
		conexion.commit()
	except psycopg2.errors.UniqueViolation:
		conexion.rollback()
	cursor.close()
	conexion.close()

def evento_existe(url):
	conexion = get_conexion()
	cursor = conexion.cursor()
	cursor.execute("SELECT 1 FROM eventos_mercado WHERE url = %s", (url,))
	resultado = cursor.fetchone()
	cursor.close()
	conexion.close()
	return resultado is not None

def cargar_ultimo(tabla):
	conexion = get_conexion()
	query = f"SELECT * FROM {tabla} ORDER BY fecha DESC LIMIT 1"
	df = pd.read_sql_query(query, conexion)
	conexion.close()
	if df.empty:
		return None
	return df.iloc[0]

def cargar_historial(tabla, limite=100):
	conexion = get_conexion()
	query = f"SELECT * FROM {tabla} ORDER BY fecha ASC LIMIT {limite}"
	df = pd.read_sql_query(query, conexion)
	conexion.close()
	return df

def cargar_eventos(limite=50):
	conexion = get_conexion()
	query = f"SELECT * FROM eventos_mercado ORDER BY fecha_noticia DESC LIMIT {limite}"
	df = pd.read_sql_query(query, conexion)
	conexion.close()
	return df