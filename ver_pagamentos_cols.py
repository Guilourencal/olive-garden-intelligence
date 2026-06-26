import psycopg2
from db import get_conn

conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='ifood_pagamentos' ORDER BY ordinal_position")
print('Colunas:', [r[0] for r in cur.fetchall()])
cur.execute("SELECT * FROM ifood_pagamentos LIMIT 2")
for row in cur.fetchall():
    print(row)
cur.close()
conn.close()
