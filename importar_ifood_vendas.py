import pandas as pd
import psycopg2
import os
import glob
from datetime import datetime

PASTA = "data/ifood_vendas"

conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()

# Cria tabelas
cur.execute("""
    CREATE TABLE IF NOT EXISTS ifood_vendas (
        id SERIAL PRIMARY KEY,
        periodo VARCHAR(100),
        filial VARCHAR(255),
        logistica VARCHAR(100),
        pedidos INTEGER,
        faturamento FLOAT,
        taxa_entrega FLOAT,
        ticket_medio FLOAT,
        novos_clientes INTEGER,
        arquivo_origem VARCHAR(255),
        importado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(periodo, filial, logistica)
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS ifood_horarios (
        id SERIAL PRIMARY KEY,
        periodo VARCHAR(100),
        filial VARCHAR(255),
        periodo_semana VARCHAR(50),
        horario VARCHAR(20),
        pedidos INTEGER,
        arquivo_origem VARCHAR(255),
        UNIQUE(periodo, filial, periodo_semana, horario)
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS ifood_pagamentos (
        id SERIAL PRIMARY KEY,
        periodo VARCHAR(100),
        filial VARCHAR(255),
        forma_pagamento VARCHAR(100),
        pedidos INTEGER,
        arquivo_origem VARCHAR(255),
        UNIQUE(periodo, filial, forma_pagamento)
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS ifood_dias (
        id SERIAL PRIMARY KEY,
        periodo VARCHAR(100),
        filial VARCHAR(255),
        dia_semana VARCHAR(20),
        pedidos INTEGER,
        arquivo_origem VARCHAR(255),
        UNIQUE(periodo, filial, dia_semana)
    )
""")

conn.commit()
print("Tabelas criadas!")

MAPA_FILIAIS = {
    'Olive Garden - Shopping Morumbi': 'Olive Garden - Morumbi',
    'Olive Garden - Shopping Center Norte': 'Olive Garden - Center Norte',
    'Olive Garden - Shopping Parque Dom Pedro': 'Olive Garden - Dom Pedro',
    'Olive Garden  - Shopping Aricanduva': 'Olive Garden - Aricanduva',
    'Olive Garden - Shopping Aricanduva': 'Olive Garden - Aricanduva',
    'Olive Garden - Guarulhos GRU2': 'Olive Garden - Guarulhos GRU2',
    'Olive Garden - Guarulhos GRU3': 'Olive Garden - Guarulhos GRU3',
}

def normalizar_filial(nome):
    nome = str(nome).strip()
    for k, v in MAPA_FILIAIS.items():
        if k.lower() in nome.lower():
            return v
    return nome

arquivos = glob.glob(os.path.join(PASTA, "iFood_Vendas_*.xlsx"))
print(f"\nArquivos encontrados: {len(arquivos)}")

for arquivo in arquivos:
    nome = os.path.basename(arquivo)
    print(f"\nImportando: {nome}")
    
    # Vendas
    df = pd.read_excel(arquivo, sheet_name='Vendas', header=0)
    df.columns = ['periodo','marca','servico','logistica','id_loja','filial','estado','cidade','pedidos','faturamento','taxa_entrega','ticket_medio','novos_clientes']
    ins = dup = 0
    for _, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO ifood_vendas (periodo, filial, logistica, pedidos, faturamento, taxa_entrega, ticket_medio, novos_clientes, arquivo_origem)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (periodo, filial, logistica) DO NOTHING
            """, (str(row['periodo']), normalizar_filial(str(row['filial'])), str(row['logistica']),
                  int(row['pedidos']) if pd.notna(row['pedidos']) else 0,
                  float(row['faturamento']) if pd.notna(row['faturamento']) else 0,
                  float(row['taxa_entrega']) if pd.notna(row['taxa_entrega']) else 0,
                  float(row['ticket_medio']) if pd.notna(row['ticket_medio']) else 0,
                  int(row['novos_clientes']) if pd.notna(row['novos_clientes']) else 0,
                  nome))
            if cur.rowcount > 0: ins += 1
            else: dup += 1
        except Exception as e:
            conn.rollback()
    conn.commit()
    print(f"  Vendas: {ins} inseridos | {dup} duplicatas")

    # Horarios
    df_h = pd.read_excel(arquivo, sheet_name='Horário com mais vendas', header=0)
    df_h.columns = ['periodo','marca','servico','logistica','id_loja','filial','estado','cidade','periodo_semana','horario','pedidos']
    ins = dup = 0
    for _, row in df_h.iterrows():
        try:
            cur.execute("""
                INSERT INTO ifood_horarios (periodo, filial, periodo_semana, horario, pedidos, arquivo_origem)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (periodo, filial, periodo_semana, horario) DO NOTHING
            """, (str(row['periodo']), normalizar_filial(str(row['filial'])),
                  str(row['periodo_semana']), str(row['horario']),
                  int(row['pedidos']) if pd.notna(row['pedidos']) else 0, nome))
            if cur.rowcount > 0: ins += 1
            else: dup += 1
        except Exception as e:
            conn.rollback()
    conn.commit()
    print(f"  Horarios: {ins} inseridos | {dup} duplicatas")

    # Pagamentos
    df_p = pd.read_excel(arquivo, sheet_name='Formas de pagamento utilizadas', header=0)
    df_p.columns = ['periodo','marca','servico','logistica','id_loja','filial','estado','cidade','forma_pagamento','pedidos']
    ins = dup = 0
    for _, row in df_p.iterrows():
        try:
            cur.execute("""
                INSERT INTO ifood_pagamentos (periodo, filial, forma_pagamento, pedidos, arquivo_origem)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (periodo, filial, forma_pagamento) DO NOTHING
            """, (str(row['periodo']), normalizar_filial(str(row['filial'])),
                  str(row['forma_pagamento']),
                  int(row['pedidos']) if pd.notna(row['pedidos']) else 0, nome))
            if cur.rowcount > 0: ins += 1
            else: dup += 1
        except Exception as e:
            conn.rollback()
    conn.commit()
    print(f"  Pagamentos: {ins} inseridos | {dup} duplicatas")

    # Dias
    df_d = pd.read_excel(arquivo, sheet_name='Dias com mais vendas', header=0)
    df_d.columns = ['periodo','marca','servico','logistica','id_loja','filial','estado','cidade','dia_semana','pedidos']
    ins = dup = 0
    for _, row in df_d.iterrows():
        try:
            cur.execute("""
                INSERT INTO ifood_dias (periodo, filial, dia_semana, pedidos, arquivo_origem)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (periodo, filial, dia_semana) DO NOTHING
            """, (str(row['periodo']), normalizar_filial(str(row['filial'])),
                  str(row['dia_semana']),
                  int(row['pedidos']) if pd.notna(row['pedidos']) else 0, nome))
            if cur.rowcount > 0: ins += 1
            else: dup += 1
        except Exception as e:
            conn.rollback()
    conn.commit()
    print(f"  Dias: {ins} inseridos | {dup} duplicatas")

cur.execute("SELECT COUNT(id) FROM ifood_vendas")
print(f"\n✅ Total ifood_vendas: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(id) FROM ifood_horarios")
print(f"✅ Total ifood_horarios: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(id) FROM ifood_pagamentos")
print(f"✅ Total ifood_pagamentos: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(id) FROM ifood_dias")
print(f"✅ Total ifood_dias: {cur.fetchone()[0]}")

cur.close()
conn.close()
print("\nImportacao concluida!")
