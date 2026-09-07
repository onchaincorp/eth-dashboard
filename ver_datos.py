import sqlite3
import pandas as pd

conexion = sqlite3.connect("eth_dashboard.db")

df_precios = pd.read_sql_query("SELECT * FROM precios_eth", conexion)
conexion.close()

print(df_precios)