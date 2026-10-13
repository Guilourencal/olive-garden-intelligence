from db import get_conn
conn = get_conn()
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS keeta_diario (
        id SERIAL PRIMARY KEY,
        data DATE NOT NULL,
        filial VARCHAR(100) NOT NULL,
        ganhos_liquidos NUMERIC(12,2) DEFAULT 0,
        vendas_itens NUMERIC(12,2) DEFAULT 0,
        outros_ganhos NUMERIC(12,2) DEFAULT 0,
        despesa NUMERIC(12,2) DEFAULT 0,
        comissao NUMERIC(12,2) DEFAULT 0,
        outras_despesas NUMERIC(12,2) DEFAULT 0,
        arquivo_origem VARCHAR(200),
        importado_em TIMESTAMP DEFAULT NOW(),
        UNIQUE(data, filial)
    )
""")
conn.commit()
print("Tabela keeta_diario criada/verificada OK")
conn.close()
