import psycopg2
from db import get_conn
conn = get_conn()
cur = conn.cursor()
cur.execute("ALTER TABLE reviews ADD COLUMN IF NOT EXISTS fonte_id VARCHAR(255)")
cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS reviews_fonte_id_idx ON reviews(fonte_id) WHERE fonte_id IS NOT NULL")
conn.commit()
print('Coluna fonte_id adicionada!')
cur.close()
conn.close()
