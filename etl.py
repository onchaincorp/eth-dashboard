from datetime import datetime
from fetchers import obtener_precio_eth, obtener_gas_fees, obtener_tvl, obtener_stablecoin_supply, obtener_eth_staking, obtener_tx_count, obtener_active_addresses
from database import crear_tabla, guardar_precio, guardar_gas, guardar_defillama, guardar_staking, guardar_network_activity

#
def correr_etl():
	crear_tabla()

	precio, cambio, marketcap = obtener_precio_eth()
	fecha_actual = datetime.now().isoformat()

	guardar_precio(precio, cambio, marketcap, fecha_actual)

	print(f"Guardado: 1 ETH = ${precio} USD ({cambio:.2f}%) a las {fecha_actual}")

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

	stake = obtener_eth_staking()
	fecha_actual = datetime.now().isoformat()

	guardar_staking(stake, fecha_actual)

	print(f"Guardado: {stake} ETH staked a las {fecha_actual}")

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






