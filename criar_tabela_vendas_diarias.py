import psycopg2
from db import get_conn
conn = get_conn()
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS vendas_diarias (
        id SERIAL PRIMARY KEY,
        data DATE NOT NULL,
        filial VARCHAR(50) NOT NULL,
        ano INTEGER,
        mes VARCHAR(10),
        dia_semana VARCHAR(10),
        semana VARCHAR(50),
        venda_salao FLOAT,
        gc_salao INTEGER,
        venda_dlv FLOAT,
        gc_dlv INTEGER,
        venda_togo FLOAT,
        gc_togo INTEGER,
        venda_total FLOAT,
        meta_venda FLOAT,
        venda_ano1 FLOAT,
        ticket_total FLOAT,
        pct_salao FLOAT,
        pct_dlv FLOAT,
        pct_togo FLOAT,
        hdc INTEGER,
        venda_por_hdc FLOAT,
        importado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(data, filial)
    )
""")
conn.commit()
print('Tabela vendas_diarias criada!')
cur.close()
conn.close()
