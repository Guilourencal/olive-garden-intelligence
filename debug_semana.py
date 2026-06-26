import pandas as pd
from db import get_conn
import psycopg2
from datetime import timedelta

conn = get_conn()
df = pd.read_sql("SELECT * FROM vendas_diarias ORDER BY data, filial", conn)
conn.close()

df["data_dt"] = pd.to_datetime(df["data"])
hoje_dt = df["data_dt"].max()
print(f"Data maxima: {hoje_dt}")

dias_desde_dom = (hoje_dt.weekday() + 1) % 7
ultimo_dom = hoje_dt - timedelta(days=dias_desde_dom)
ultima_seg = ultimo_dom - timedelta(days=6)
print(f"Ultima semana: {ultima_seg.date()} a {ultimo_dom.date()}")

seg_ano1 = ultima_seg - timedelta(days=364)
dom_ano1 = ultimo_dom - timedelta(days=364)
print(f"Mesma semana ano anterior: {seg_ano1.date()} a {dom_ano1.date()}")

df_ult = df[(df["data_dt"] >= ultima_seg) & (df["data_dt"] <= ultimo_dom)]
df_ano1 = df[(df["data_dt"] >= seg_ano1) & (df["data_dt"] <= dom_ano1)]
print(f"Registros semana atual: {len(df_ult)}")
print(f"Registros ano anterior: {len(df_ano1)}")
print(f"Range de datas no banco: {df['data_dt'].min().date()} a {df['data_dt'].max().date()}")
