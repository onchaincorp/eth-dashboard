import streamlit as st
import pandas as pd
from io import BytesIO
import sys
from database import cargar_ultimo, cargar_historial, crear_tabla

from datetime import datetime, timedelta
from etl import correr_etl

def datos_estan_viejos(fecha_texto, minutos=60):
	fecha_dato = datetime.fromisoformat(fecha_texto)
	return datetime.now() - fecha_dato > timedelta(minutes=minutos)

crear_tabla()

ultimo_precio = cargar_ultimo("precios_eth")
if ultimo_precio is None or datos_estan_viejos(ultimo_precio["fecha"]):
	with st.spinner("Actualizando datos desde las APIS..."):
		correr_etl()

# ---configuracion de la pagina ---

st.set_page_config(
	page_title="Dashboard Financiero de Ethereum",
	page_icon="⟠",
	layout="wide",
)

# --- Estilo tipo Apple ---

st.markdown("""
	<style>
	.stMetric {
		background-color: #F5F5F7;
		border-radius: 18px;
		paddinng: 20px 24px;
		box-shadow: 0 1px 3px rgba(0,0,0,0.04);
	}
	.stMetric label {
		font-weight: 500;
		color: #6E6E73;
	}
	div[data-testid="stMetricValue"] {
		font-size: 32px;
		font-weight: 600;
		color: #1D1D1F;
	}
	h1 {
		font-weight: 600;
		letter-spacing: -0.5px;
	}
	</style>
""", unsafe_allow_html=True)

# --- Encabezado con logo ---

col_logo, col_titulo, col_actualizado = st.columns([0.5, 2.5, 1])
with col_titulo:
	st.image(
		"https://upload.wikimedia.org/wikipedia/commons/0/05/Ethereum_logo_2014.svg",
		width=60,
	)
with col_titulo:
	st.title("Ethereum - Panel Financiero")
	st.caption("Métricas on-chain y de mercado, actualizadas en tiempo real")

# --- Cargar datos más recientes ---

precio = cargar_ultimo("precios_eth")
gas = cargar_ultimo("gas_fees")
defillama = cargar_ultimo("defillama_metrics")
staking = cargar_ultimo("staking_metrics")
network = cargar_ultimo("network_activity")

if network is None:
	network = {"tx_count": 0, "active_addresses": 0}

if precio is None:
	st.warning("Todavía no hay datos. Corre 'python etl.py' desde tu terminal primero.")
	st.stop()
	
with col_actualizado:
	st.metric("Última actualizacion", precio["fecha"][11:19] + " UTC")

st.divider()

# --- Fila 1: Precio, Market Cap, Gas ---

col1, col2, col3 = st.columns(3)

col1.metric(
	"Precio ETH",
	f"${precio['precio_usd']:,.2f}",
	delta=f"{precio['cambio_24h']:.2f}%",
)
col2.metric(
	"Market Cap",
	f"${precio['market_cap']/1e9:,.2f}B",
)
col3.metric(
	"Gas Price",
	f"{gas['gas_gwei']:.3f} Gwei",
)

# --- Fila 2: TVL, Stablecoins, Staking ---

col4, col5, col6 = st.columns(3)

col4.metric(
	"TVL (DeFi)",
	f"${defillama['tvl_usd']/1e9:,.2f}B",
)
col5.metric(
	"Stablecoin Supply",
	f"${defillama['stablecoin_supply_usd']/1e9:,.2f}B",
)
col6.metric(
	"ETH en Staking",
	f"{staking['eth_staked']/1e6:,.2f}M ETH",
)

# --- Fila 3: Actividad de red ---

col7, col8 = st.columns(2)

col7.metric(
	"Transacciones (día)",
	f"{network['tx_count']:,.0f}",
)
col8.metric(
	"Direcciones activas", 
	f"{network['active_addresses']:,.0f}",
)

st.divider()

# --- Gráficas historicas en pestañas ---

st.subheader("Tendencias históricas")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💰 Precio", "⛽ Gas", "🏦 DeFi", "🔒 Staking", "📡 Red"])

with tab1:
	historial_precio = cargar_historial("precios_eth")
	if len(historial_precio) >= 2:
		st.line_chart(historial_precio.set_index("fecha")["precio_usd"])
	else:
		st.info("Corre el ETL varias veces para ver tendencia aquí.")
with tab2:
	historial_gas = cargar_historial("gas_fees")
	if len(historial_gas) >= 2:
		st.line_chart(historial_gas.set_index("fecha")["gas_gwei"])	
	else:
		st.info("Corre el ETL varias veces para ver tendencia aquí.")

with tab3:
	historial_defi = cargar_historial("defillama_metrics")
	if len(historial_defi) >= 2:
		col_tvl, col_stable = st.columns(2)
		with col_tvl:
			st.caption("TVL (Total Value Locked)")
			st.line_chart(historial_defi.set_index("fecha")["tvl_usd"])
		with col_stable:
			st.caption("Stablecoin Supply")
			st.line_chart(historial_defi.set_index("fecha")["stablecoin_supply_usd"])
	else:
  		st.info("Corre el ETL varias veces para ver tendencia aquí.")

with tab4:
	historial_staking = cargar_historial("staking_metrics")
	if len(historial_staking) >= 2:
 		st.line_chart(historial_staking.set_index("fecha")["eth_staked"])
	else:
  		st.info("Corre el ETL varias veces para ver tendencia aquí.")

with tab5:
	historial_red = cargar_historial("network_activity")
	if len(historial_red) >=2:
		col_tx, col_addr = st.columns(2)
		with col_tx:
			st.caption("Transacciones diarias")
			st.line_chart(historial_red.set_index("fecha")["tx_count"])
		with col_addr:
			st.caption("Direcciones activas")
			st.line_chart(historial_red.set_index("fecha")["active_addresses"])
	else:
		st.info("Corre el ETL varias veces para ver tendencia aquí.")

with st.expander("Ver datos crudos (precio)"):
	st.dataframe(historial_precio, use_container_width=True)

st.divider()

def generar_reporte_excel():
	buffer = BytesIO()

	hist_precio = cargar_historial("precios_eth", limite=100000)
	hist_gas = cargar_historial("gas_fees", limite=100000)
	hist_defi = cargar_historial("defillama_metrics", limite=100000)
	hist_staking = cargar_historial("staking_metrics", limite=100000)
	hist_red = cargar_historial("network_activity", limite=100000)

	with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
		hist_precio.to_excel(writer, sheet_name="Precio y Market Cap", index=False)
		hist_gas.to_excel(writer, sheet_name="Gas Fees", index=False)
		hist_defi.to_excel(writer, sheet_name="TVL y Stablecoins", index=False)
		hist_staking.to_excel(writer, sheet_name="Staking", index=False)
		hist_red.to_excel(writer, sheet_name="Actividad de Red", index=False)
	
	buffer.seek(0)
	return buffer

st.divider()
st.subheader("📌 Bitácora de eventos del mercado")

from database import cargar_eventos
eventos = cargar_eventos()

if eventos.empty:
	st.info("Todavía no hay eventos registrados. Se irán agregando conforme el ETL detecte noticias relevantes de Ethereum.")
else:
	for _, evento in eventos.iterrows():
		with st.expander(f"📰 {evento['titulo']}"):
			st.caption(f"Fuente: {evento['fuente']} · {evento['fecha_noticia']}")
			st.write(evento['analisis_ia'])
			st.markdown(f"[Leer noticia completa]({evento['url']})")

st.download_button(
	label="📊 Descargar datos completos (Excel)",
	data=generar_reporte_excel(),
	file_name="eth_dashboard_datos.xlsx",
	mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.caption("Fuentes: CoinGecko · Etherscan · DefiLlama · growthepie · Contrato de depósito de staking (on-chain)")

st.caption("Colaboraciones/observaciones/sugerencias via linkedin: davidpecero")