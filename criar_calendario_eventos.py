import psycopg2
from db import get_conn

conn = get_conn()
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS calendario_eventos (
        id SERIAL PRIMARY KEY,
        data_inicio DATE NOT NULL,
        data_fim DATE NOT NULL,
        filial VARCHAR(255),
        nome_evento VARCHAR(255) NOT NULL,
        tipo VARCHAR(50),
        impacto_estimado_pct FLOAT,
        recorrente BOOLEAN DEFAULT FALSE,
        mes_recorrencia INTEGER,
        observacao TEXT,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# Registrar os eventos de maio 2026
eventos = [
    ('2026-05-18', '2026-05-19', 'Olive Garden - Center Norte', 'APAS Show 2026', 'feira', None, True, 5, 'Feira APAS no Expo Center Norte — impacto positivo significativo nas vendas'),
    ('2026-05-18', '2026-05-19', 'Olive Garden - Dom Pedro', 'Prato em Dobro — Shopping Dom Pedro', 'promocao_shopping', None, False, None, 'Acao patrocinada pelo Shopping Dom Pedro — impacto positivo nas vendas'),
]

for ev in eventos:
    cur.execute("""
        INSERT INTO calendario_eventos (data_inicio, data_fim, filial, nome_evento, tipo, impacto_estimado_pct, recorrente, mes_recorrencia, observacao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, ev)

conn.commit()
cur.execute('SELECT id, data_inicio, data_fim, filial, nome_evento, tipo, recorrente FROM calendario_eventos ORDER BY data_inicio')
print('=== CALENDARIO DE EVENTOS ===')
for row in cur.fetchall():
    print(f'  [{row[0]}] {row[1]} a {row[2]} | {row[3].replace("Olive Garden - ","")} | {row[4]} | {row[5]} | recorrente={row[6]}')
cur.close()
conn.close()
print('OK')
