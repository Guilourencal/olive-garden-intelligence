import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()

df = pd.read_sql("SELECT texto FROM reviews WHERE plataforma = 'Google Reviews' LIMIT 5", conn)
print(df["texto"].to_string())
conn.close()