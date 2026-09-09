from datetime import datetime
from fetchers import obtener_precio_eth, obtener_gas_fees, obtener_tvl, obtener_stablecoin_supply, obtener_eth_staking, obtener_tx_count, obtener_active_addresses
from database import crear_tabla, guardar_precio, guardar_gas, guardar_defillama, guardar_staking, guardar_network_activity
from fetchers import obtener_noticias_eth, generar_analisis_evento
from database import guardar_evento, evento_existe

#
def correr_etl():
	crear_tabla()

	precio, cambio, marketcap = obtener_precio_eth()
	fecha_actual = datetime.now().isoformat()

	guardar_precio(precio, cambio, marketcap, fecha_actual)

	print(f"Guardado: 1 ETH = ${precio} USD ({cambio:.2f}%) a las {fecha_actual}")

	try:
		procesar_eventos_mercado()
	except Exception as e:
		print(f"No se pudo procesar eventos de mercado: {e}")

def procesar_eventos_mercado():
	noticias = obtener_noticias_eth()
	ultimo_precio = None

	try:
		import sqlite3
		conexion = sqlite3.connect("eth_dashboard.db")
		cursor = conexion.cursor()
		cursor.execute("SELECT * FROM precios_eth ORDER BY fecha DESC LIMIT 1")
		fila = cursor.fetchone()
		conexion.close()
		if fila:
			ultimo_precio = {"precio": fila[1], "cambio": fila[2]}
	except Exception:
		pass

	if ultimo_precio is None:
		print("No hay precio reciente, se omite el análisis de eventos.")
		return
	ultimo_gas = obtener_gas_fees()

	for noticia in noticias:
		url = noticia.get("link")
		if not url or evento_existe(url):
			continue

		titulo = noticia.get("title", "")
		descripcion = noticia.get("description", "")
		
		texto_completo = (titulo + " " + descripcion).lower()
		if "ethereum" not in texto_completo and " eth " not in texto_completo:
			continue

		fecha_noticia = noticia.get("pubDate", "")

		try:
			analisis = generar_analisis_evento(
				titulo, descripcion,
				ultimo_precio["precio"], ultimo_precio["cambio"],
				ultimo_gas
			)
			guardar_evento(
				fecha_noticia, titulo, noticia.get("source", ""),
				url, analisis, datetime.now().isoformat()
			)
			print(f"Evento guardado: {titulo}")
		except Exception as e:
			print(f"No se pudo analizar la noticia '{titulo}': {e}")
	
#

	gas = obtener_gas_fees()
	fecha_actual = datetime.now().isoformat()

	guardar_gas(gas, fecha_actual)

	print(f"Guardado: 1 unidad de Gas = {gas} Gwei a las {fecha_actual}")

#

	tvl = obtener_tvl()
	stablecoins = obtener_stablecoin_supply()
	fecha_actual = datetime.now().isoformat()

	guardar_defillama(tvl, stablecoins, fecha_actual)

	print(f"Guardado: TVL ${tvl} / Stablecoins ${stablecoins} a las {fecha_actual}")

#

try:
	stake = obtener_eth_staking()
	fecha_actual = datetime.now().isoformat()

	guardar_staking(stake, fecha_actual)

	print(f"Guardado: {stake} ETH staked a las {fecha_actual}")
except Exception as e:
	print(f"No se pudo guardar ETH stakinh: {e}")

#

try:
	tx = obtener_tx_count()
	addresses = obtener_active_addresses()
	fecha_actual = datetime.now().isoformat()

	guardar_network_activity(tx, addresses, fecha_actual)

	print(f"Guardado: {tx} tx / {addresses} active addresses a las {fecha_actual}")
except Exception as e:
	print(f"No se pudo guardar actividad de red: {e}")
if __name__ == "__main__":
	correr_etl()






