import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
df = pd.read_sql('SELECT * FROM ifood_vendas WHERE logistica = %s ORDER BY periodo, filial', conn, params=('Entrega parceira',))
df2 = pd.read_sql('SELECT * FROM ifood_dias ORDER BY periodo, filial', conn)
df3 = pd.read_sql('SELECT * FROM ifood_horarios ORDER BY periodo, filial', conn)
conn.close()

print('=== DADOS DISPONIVEIS IFOOD ===')
print(f'Periodos: {sorted(df["periodo"].unique())}')
print(f'Registros vendas: {len(df)}')
print()
print('=== FATURAMENTO POR PERIODO ===')
fat = df.groupby('periodo').agg(fat=('faturamento','sum'), ped=('pedidos','sum')).reset_index()
for _, r in fat.iterrows():
    partes = r['periodo'].split('-')
    try:
        from datetime import datetime
        d_ini = datetime.strptime(partes[0].strip(), '%d/%m/%Y')
        d_fim = datetime.strptime(partes[1].strip(), '%d/%m/%Y')
        dias = (d_fim - d_ini).days + 1
        print(f'  {r["periodo"]}: R | {int(r["ped"])} pedidos | {dias} dias | R/dia')
    except:
        print(f'  {r["periodo"]}: R')

print()
print('=== PEDIDOS POR DIA DA SEMANA (acumulado) ===')
dow = df2.groupby('dia_semana')['pedidos'].sum().reset_index().sort_values('pedidos', ascending=False)
print(dow.to_string(index=False))
