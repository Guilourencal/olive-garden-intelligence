import psycopg2, pandas as pd, os
from datetime import datetime

conn = psycopg2.connect(host='aws-1-sa-east-1.pooler.supabase.com',port=6543,user='postgres.rvauallshhozpruvusrr',password='olivegarden2233@',database='postgres')
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS ifood_diario (
        id SERIAL PRIMARY KEY,
        data DATE NOT NULL,
        filial VARCHAR(100),
        pedidos INTEGER,
        faturamento FLOAT,
        taxa_entrega FLOAT,
        ticket_medio FLOAT,
        novos_clientes INTEGER,
        arquivo_origem VARCHAR(255),
        UNIQUE(data, filial)
    )
""")
conn.commit()
print('Tabela criada!')

pasta = r'data\ifood_diario'
os.makedirs(pasta, exist_ok=True)
arquivos = [f for f in os.listdir(pasta) if f.endswith('.xlsx') or f.endswith('.xls')]
print(f'Arquivos encontrados: {len(arquivos)}')

total_ins = total_dup = 0
for arquivo in sorted(arquivos):
    caminho = os.path.join(pasta, arquivo)
    df = pd.read_excel(caminho, sheet_name='Vendas')
    df = df[df['Logística'] == 'Entrega parceira']
    ins = dup = 0
    for _, row in df.iterrows():
        try:
            periodo = str(row['Período'])
            data = datetime.strptime(periodo.split('-')[0].strip(), '%d/%m/%Y').date()
            filial = str(row['Nome da loja'])
            cur.execute("""
                INSERT INTO ifood_diario (data, filial, pedidos, faturamento, taxa_entrega, ticket_medio, novos_clientes, arquivo_origem)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (data, filial) DO UPDATE SET
                    pedidos=EXCLUDED.pedidos, faturamento=EXCLUDED.faturamento,
                    taxa_entrega=EXCLUDED.taxa_entrega, ticket_medio=EXCLUDED.ticket_medio,
                    novos_clientes=EXCLUDED.novos_clientes
            """, (data, filial,
                int(row['Total de vendas (pedidos)']) if pd.notna(row.get('Total de vendas (pedidos)')) else 0,
                float(row['Valor total de vendas']) if pd.notna(row.get('Valor total de vendas')) else 0,
                float(row['Taxa de entrega']) if pd.notna(row.get('Taxa de entrega')) else 0,
                float(row['Ticket médio']) if pd.notna(row.get('Ticket médio')) else 0,
                int(row['Novos clientes']) if pd.notna(row.get('Novos clientes')) else 0,
                arquivo))
            if cur.rowcount > 0: ins += 1
            else: dup += 1
        except Exception as e:
            print(f'  Erro: {e}')
    conn.commit()
    print(f'  {arquivo}: {ins} inseridos | {dup} atualizados')
    total_ins += ins; total_dup += dup

cur.execute('SELECT COUNT(*), MIN(data), MAX(data) FROM ifood_diario')
r = cur.fetchone()
print(f'\nBanco: {r[0]} registros | {r[1]} a {r[2]}')
cur.close()
conn.close()
print('Concluido!')
