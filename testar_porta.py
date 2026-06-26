import psycopg2
from db import get_conn
conn = get_conn()
print('Conectado!')
conn.close()
