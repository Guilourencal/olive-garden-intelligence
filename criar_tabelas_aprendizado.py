import psycopg2
from db import get_conn

conn = get_conn()
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS projecoes_historico (
        id SERIAL PRIMARY KEY,
        data_projecao DATE NOT NULL,
        filial VARCHAR(255) NOT NULL,
        data_alvo DATE NOT NULL,
        valor_projetado FLOAT,
        valor_realizado FLOAT,
        erro_absoluto FLOAT,
        erro_pct FLOAT,
        fator_dow FLOAT,
        fator_mes FLOAT,
        fator_rec FLOAT,
        peso_stl FLOAT,
        peso_a1 FLOAT,
        modelo VARCHAR(50) DEFAULT 'ensemble_stl_v1',
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(data_projecao, filial, data_alvo)
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS modelo_parametros (
        id SERIAL PRIMARY KEY,
        filial VARCHAR(255) NOT NULL,
        parametro VARCHAR(100) NOT NULL,
        valor FLOAT NOT NULL,
        amostras INTEGER,
        mape_historico FLOAT,
        bias_historico FLOAT,
        atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(filial, parametro)
    )
""")

conn.commit()
cur.close()
conn.close()
print('Tabelas criadas com sucesso!')
print('  projecoes_historico — registra projecoes e erros realizados')
print('  modelo_parametros — armazena parametros calibrados por filial')
