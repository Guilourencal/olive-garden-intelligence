import psycopg2
from db import get_conn
from datetime import date

conn = get_conn()
cur = conn.cursor()

cur.execute("""
    INSERT INTO calendario_eventos (data_inicio, data_fim, filial, nome_evento, tipo, recorrente, mes_recorrencia, observacao)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", ('2026-05-26', '2026-05-31', None, 'Ultima semana do mes — queda sazonal', 'outro', False, None,
      'Ultima semana do mes com queda sistematica por menor disponibilidade de renda. Padrao recorrente todo mes — registrar manualmente a cada ciclo.'))

conn.commit()
cur.close()
conn.close()
print('Evento registrado!')
