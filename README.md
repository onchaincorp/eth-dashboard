\# ⟠ ETH Financial Dashboard



Dashboard financiero de Ethereum que extrae datos on-chain y de mercado en tiempo real, los almacena en SQLite, y los visualiza en un panel interactivo con Streamlit.



\## Métricas incluidas



| Métrica | Fuente |

|---|---|

| Precio ETH (USD) | CoinGecko |

| Market cap | CoinGecko |

| Gas fees (Gwei) | Etherscan API v2 |

| TVL (Total Value Locked) | DefiLlama |

| Stablecoin supply en Ethereum | DefiLlama |

| ETH en staking | Balance del contrato de depósito on-chain (vía Etherscan) |

| Número de transacciones (24h) | growthepie |

| Direcciones activas (24h) | growthepie |

| Volumen de transacciones (USD) | ⚠️ Pendiente — sin fuente gratuita confiable, ver \[Roadmap](#roadmap) |



\## Stack técnico



Python · Pandas · SQLite · Streamlit · APIs REST



\## Estructura del proyecto



\## Instalación



```bash

git clone https://github.com/onchaincorp/eth-dashboard.git

cd eth-dashboard

python -m venv .venv

.venv\\Scripts\\activate       # En Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt

```



Crea un archivo `.env` en la raíz del proyecto con tu API key gratuita de Etherscan:



(Consíguela gratis en \[etherscan.io/myapikey](https://etherscan.io/myapikey))



\## Uso



Cargar el primer snapshot de datos:

```bash

python etl.py

```



Levantar el dashboard:

```bash

streamlit run app.py

```



\## Automatización



`run\_etl.bat` permite programar la extracción de datos con el Programador de Tareas de Windows, para que el historial se acumule solo sin correr el script manualmente.



\## Roadmap



\- \[ ] Volumen de transacciones (USD) vía Dune Analytics

\- \[ ] Migrar de SQLite a Postgres para uso en producción

\- \[ ] Desplegar en Streamlit Community Cloud



\## Autor



David Pecero — \[LinkedIn](https://www.linkedin.com/in/davidpecero)

