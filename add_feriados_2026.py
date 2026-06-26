import psycopg2
from db import get_conn
from datetime import date

conn = get_conn()
cur = conn.cursor()

eventos = [
    ('2026-06-03', '2026-06-03', None, 'Vespera Corpus Christi — movimento elevado', 'feriado', False, None, 'Vespera de feriado nacional — historico mostra aumento significativo'),
    ('2026-06-04', '2026-06-04', None, 'Corpus Christi', 'feriado', True, 6, 'Feriado nacional — vendas 2-4x acima do normal em todas as filiais'),
    ('2026-06-05', '2026-06-05', None, 'Pos Corpus Christi — movimento elevado', 'feriado', False, None, 'Dia apos feriado prolongado — movimento ainda acima do normal'),
    ('2026-09-07', '2026-09-07', None, 'Independencia do Brasil', 'feriado', True, 9, 'Feriado nacional'),
    ('2026-10-12', '2026-10-12', None, 'Nossa Senhora Aparecida', 'feriado', True, 10, 'Feriado nacional'),
    ('2026-11-02', '2026-11-02', None, 'Finados', 'feriado', True, 11, 'Feriado nacional'),
    ('2026-11-15', '2026-11-15', None, 'Proclamacao da Republica', 'feriado', True, 11, 'Feriado nacional'),
    ('2026-11-20', '2026-11-20', None, 'Consciencia Negra', 'feriado', True, 11, 'Feriado nacional'),
    ('2026-12-25', '2026-12-25', None, 'Natal', 'feriado', True, 12, 'Feriado nacional'),
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
