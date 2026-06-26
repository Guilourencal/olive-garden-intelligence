import psycopg2
from db import get_conn
from datetime import date

conn = get_conn()
cur = conn.cursor()

eventos = [
    ('2026-06-08', '2026-06-28', None, 'Copa do Mundo 2026 — Fase de Grupos', 'evento_externo', False, None, 'Copa do Mundo afeta movimento — queda sistematica especialmente em dias de jogo do Brasil'),
    ('2026-06-11', '2026-06-11', None, 'Copa do Mundo — Jogo Brasil', 'evento_externo', False, None, 'Jogo do Brasil na Copa 2026 — queda forte de movimento'),
    ('2026-06-15', '2026-06-15', None, 'Copa do Mundo — Jogo Brasil', 'evento_externo', False, None, 'Jogo do Brasil na Copa 2026 — queda forte de movimento'),
    ('2026-06-19', '2026-06-19', None, 'Copa do Mundo — Jogo Brasil', 'evento_externo', False, None, 'Jogo do Brasil na Copa 2026 — queda forte de movimento'),
]

for ev in eventos:
    cur.execute("""
        INSERT INTO calendario_eventos (data_inicio, data_fim, filial, nome_evento, tipo, recorrente, mes_recorrencia, observacao)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT DO NOTHING
    """, ev)

conn.commit()
cur.close()
conn.close()
print(f'OK — {len(eventos)} eventos registrados')
