import psycopg2
from db import get_conn
from datetime import date

conn = get_conn()
cur = conn.cursor()
cur.execute("DELETE FROM projecoes_historico WHERE valor_realizado IS NULL")
deleted = cur.rowcount
conn.commit()
cur.close()
conn.close()
print(f'OK — {deleted} projecoes futuras deletadas')
