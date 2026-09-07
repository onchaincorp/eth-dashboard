import streamlit as st
import sys
from database import cargar_ultimo, cargar_historial

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

tab1, tab2, tab3, tab4 = st.tabs(["💰 Precio", "⛽ Gas", "🏦 DeFi", "🔒 Staking"])

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

with st.expander("Ver datos crudos (precio)"):
	st.dataframe(historial_precio, use_container_width=True)

st.caption("Fuentes: CoinGecko · Etherscan · DefiLlama · growthepie · Contrato de depósito de staking (on-chain)")

st.caption("Colaboraciones/observaciones/sugerencias via linkedin: davidpecero")