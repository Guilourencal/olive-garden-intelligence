import psycopg2
from db import get_conn
from datetime import date

conn = get_conn()
cur = conn.cursor()

eventos = [
    ('2026-05-20', '2026-05-20', 'Olive Garden - Center Norte', 'APAS Show 2026', 'feira', True, 5, 'Extensao do evento APAS no Expo Center Norte'),
    ('2026-05-20', '2026-05-20', 'Olive Garden - Dom Pedro', 'Prato em Dobro — Shopping Dom Pedro', 'promocao_shopping', False, None, 'Extensao da acao patrocinada pelo Shopping Dom Pedro'),
    ('2026-05-20', '2026-05-20', 'Olive Garden - Aricanduva', 'Dia atipico sem causa identificada', 'outro', False, None, 'Venda significativamente acima do esperado sem causa identificada'),
]

for ev in eventos:
    cur.execute("""
        INSERT INTO calendario_eventos (data_inicio, data_fim, filial, nome_evento, tipo, recorrente, mes_recorrencia, observacao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, ev)
    print(f'Registrado: {ev[3]} — {ev[2].replace("Olive Garden - ","")} — {ev[0]}')

conn.commit()
cur.close()
conn.close()
print('OK')
