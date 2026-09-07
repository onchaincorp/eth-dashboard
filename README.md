# ETH Financial Dashboard

Dashboard financiero de Ethereum que extrae datos on-chain y de mercado en tiempo real, los almacena en SQLite, y los visualiza en un panel interactivo con Streamlit.

## Metricas incluidas

- Precio ETH (USD) - CoinGecko
- Market cap - CoinGecko
- Gas fees (Gwei) - Etherscan API v2
- TVL (Total Value Locked) - DefiLlama
- Stablecoin supply en Ethereum - DefiLlama
- ETH en staking - Balance del contrato de deposito on-chain (via Etherscan)
- Numero de transacciones (24h) - growthepie
- Direcciones activas (24h) - growthepie
- Volumen de transacciones (USD) - Pendiente, sin fuente gratuita confiable

## Stack tecnico

Python, Pandas, SQLite, Streamlit, APIs REST

## Instalacion

git clone https://github.com/onchaincorp/eth-dashboard.git
cd eth-dashboard
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

Crea un archivo .env en la raiz del proyecto con tu API key gratuita de Etherscan:
ETHERSCAN_API_KEY=tu_key_aqui

Consiguela gratis en https://etherscan.io/myapikey

## Uso

Cargar el primer snapshot de datos:
python etl.py

Levantar el dashboard:
streamlit run app.py

## Automatizacion

run_etl.bat permite programar la extraccion de datos con el Programador de Tareas de Windows, para que el historial se acumule solo sin correr el script manualmente.

## Roadmap

- Volumen de transacciones (USD) via Dune Analytics
- Migrar de SQLite a Postgres para uso en produccion
- Desplegar en Streamlit Community Cloud

## Autor

David Pecero - LinkedIn: https://www.linkedin.com/in/davidpecero
