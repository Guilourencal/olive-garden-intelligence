import psycopg2
conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS ifood_tags (
        id SERIAL PRIMARY KEY,
        periodo VARCHAR(100),
        filial VARCHAR(255),
        tag VARCHAR(100),
        tipo VARCHAR(20),
        total_sim INTEGER,
        total_nao INTEGER,
        pct_sim FLOAT,
        importado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(periodo, filial, tag)
    )
""")
conn.commit()
print('Tabela ifood_tags criada!')
cur.close()
conn.close()
