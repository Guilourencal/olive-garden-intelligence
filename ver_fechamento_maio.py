import psycopg2
from db import get_conn
import pandas as pd
from datetime import date

conn = get_conn()

# Vendas salao maio 2026
df_vd = pd.read_sql("""
    SELECT data, filial, venda_salao, venda_total, gc_salao, meta_venda, venda_ano1, ticket_total, hdc, venda_por_hdc
    FROM vendas_diarias
    WHERE EXTRACT(month FROM data)=5 AND EXTRACT(year FROM data)=2026
    ORDER BY data, filial
""", conn)

# iFood maio 2026
df_if = pd.read_sql("""
    SELECT filial, faturamento, pedidos, novos_clientes, logistica
    FROM ifood_vendas
    WHERE periodo LIKE '%05/2026%' AND logistica='Entrega parceira'
""", conn)

conn.close()

df_vd['filial_curta'] = df_vd['filial'].str.replace('Olive Garden - ','')
df_if['filial_curta'] = df_if['filial'].str.replace('Olive Garden - ','')

print('=== VENDAS SALAO — MAIO 2026 ===')
print(f'Periodo: {df_vd["data"].min()} a {df_vd["data"].max()}')
print()

# Totais rede
venda_total = df_vd['venda_salao'].sum()
meta_total = df_vd['meta_venda'].sum()
ano1_total = df_vd['venda_ano1'].sum()
gc_total = df_vd['gc_salao'].sum()
ticket_medio = venda_total / gc_total if gc_total > 0 else 0
pct_meta = (venda_total / meta_total - 1) * 100 if meta_total > 0 else 0
pct_ano1 = (venda_total / ano1_total - 1) * 100 if ano1_total > 0 else 0

print('--- REDE TOTAL ---')
print(f'Venda Salao:    R$ {venda_total:,.0f}'.replace(',','.'))
print(f'Meta:           R$ {meta_total:,.0f} ({pct_meta:+.1f}% vs meta)'.replace(',','.'))
print(f'Ano Anterior:   R$ {ano1_total:,.0f} ({pct_ano1:+.1f}% vs AA)'.replace(',','.'))
print(f'GCs:            {int(gc_total):,}'.replace(',','.'))
print(f'Ticket Medio:   R$ {ticket_medio:.2f}')
print()

# Por filial
print('--- POR FILIAL ---')
por_filial = df_vd.groupby('filial_curta').agg(
    venda=('venda_salao','sum'),
    meta=('meta_venda','sum'),
    ano1=('venda_ano1','sum'),
    gc=('gc_salao','sum'),
    hdc=('hdc','mean'),
    venda_por_hdc=('venda_por_hdc','mean')
).reset_index()
por_filial['pct_meta'] = (por_filial['venda']/por_filial['meta']-1)*100
por_filial['pct_ano1'] = (por_filial['venda']/por_filial['ano1']-1)*100
por_filial['ticket'] = por_filial['venda']/por_filial['gc']
for _, r in por_filial.sort_values('venda', ascending=False).iterrows():
    print(f'{r["filial_curta"]}:')
    print(f'  Venda: R$ {r["venda"]:,.0f} | Meta: {r["pct_meta"]:+.1f}% | AA: {r["pct_ano1"]:+.1f}%'.replace(',','.'))
    print(f'  GCs: {int(r["gc"]):,} | Ticket: R$ {r["ticket"]:.2f} | HDC medio: {r["hdc"]:.0f} | Venda/HDC: R$ {r["venda_por_hdc"]:.0f}'.replace(',','.'))

print()
print('=== iFOOD — MAIO 2026 ===')
ifood_total = df_if['faturamento'].sum()
pedidos_total = int(df_if['pedidos'].sum())
novos_total = int(df_if['novos_clientes'].sum())
ticket_if = ifood_total / pedidos_total if pedidos_total > 0 else 0
print(f'Faturamento:    R$ {ifood_total:,.0f}'.replace(',','.'))
print(f'Pedidos:        {pedidos_total:,}'.replace(',','.'))
print(f'Novos Clientes: {novos_total:,}'.replace(',','.'))
print(f'Ticket Medio:   R$ {ticket_if:.2f}')
print()
print('--- POR FILIAL ---')
for _, r in df_if.groupby('filial_curta').agg(
    fat=('faturamento','sum'), ped=('pedidos','sum'), nov=('novos_clientes','sum')
).reset_index().sort_values('fat', ascending=False).iterrows():
    tkt = r['fat']/r['ped'] if r['ped']>0 else 0
    print(f'{r["filial_curta"]}: R$ {r["fat"]:,.0f} | {int(r["ped"])} ped | {int(r["nov"])} novos | TM R$ {tkt:.0f}'.replace(',','.'))
