import pandas as pd
import psycopg2
import os
import glob
from datetime import datetime

PASTA = "data"

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)
cur = conn.cursor()

# Cria tabelas se não existirem
cur.execute("""
    CREATE TABLE IF NOT EXISTS pesquisa_comments (
        id SERIAL PRIMARY KEY,
        transaction_id INTEGER,
        survey_date TIMESTAMP,
        location VARCHAR(255),
        filial VARCHAR(255),
        overall_rating VARCHAR(100),
        comentario TEXT,
        arquivo_origem VARCHAR(255),
        importado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(transaction_id)
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS pesquisa_performance (
        id SERIAL PRIMARY KEY,
        restaurant VARCHAR(255),
        country VARCHAR(100),
        count INTEGER,
        overall_experience FLOAT,
        overall_dissat FLOAT,
        value FLOAT,
        service FLOAT,
        taste FLOAT,
        speed_of_service FLOAT,
        clean FLOAT,
        soup_salad_refill FLOAT,
        breadstick_refill FLOAT,
        periodo VARCHAR(100),
        arquivo_origem VARCHAR(255),
        importado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(restaurant, periodo)
    )
""")
conn.commit()
print("Tabelas criadas/verificadas!")

# Mapeia nomes de filiais para padronizar
MAPA_FILIAIS = {
    "752001 OG GRU (Terminal 3)": "Olive Garden - Guarulhos GRU3",
    "752002 OG Center Norte": "Olive Garden - Center Norte",
    "752003 OG Morumbi": "Olive Garden - Morumbi",
    "752004 OG Parque Dom Pedro": "Olive Garden - Dom Pedro",
    "752005 OG Aricanduva (Avenida Aricanduva)": "Olive Garden - Aricanduva",
    "752006 OG GRU 2 (Terminal 2)": "Olive Garden - Guarulhos GRU2",
}

def normalizar_filial(nome):
    if not isinstance(nome, str):
        return nome
    nome = nome.strip()
    for k, v in MAPA_FILIAIS.items():
        if k.lower() in nome.lower():
            return v
    return nome

# Importa Comments
comments_files = glob.glob(os.path.join(PASTA, "*OG*Comments*.xlsx")) + glob.glob(os.path.join(PASTA, "*OG Comments*.xlsx"))
print(f"\nArquivos de Comments encontrados: {len(comments_files)}")

for arquivo in comments_files:
    print(f"\nImportando: {arquivo}")
    try:
        df = pd.read_excel(arquivo, sheet_name=0)
        df.columns = [str(c).strip() for c in df.columns]

        inseridos = 0
        ignorados = 0
        for _, row in df.iterrows():
            try:
                cur.execute("""
                    INSERT INTO pesquisa_comments
                        (transaction_id, survey_date, location, filial, overall_rating, comentario, arquivo_origem)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (transaction_id) DO NOTHING
                """, (
                    row.get("Transaction #"),
                    row.get("Survey Date"),
                    row.get("Location"),
                    normalizar_filial(str(row.get("Location", ""))),
                    row.get("Overall Rating"),
                    row.get("Comment"),
                    os.path.basename(arquivo)
                ))
                if cur.rowcount > 0:
                    inseridos += 1
                else:
                    ignorados += 1
            except Exception as e:
                conn.rollback()
                print(f"  Erro linha: {e}")
        conn.commit()
        print(f"  Inseridos: {inseridos} | Ignorados (duplicatas): {ignorados}")
    except Exception as e:
        print(f"  Erro ao ler arquivo: {e}")

# Importa Performance (FW)
fw_files = glob.glob(os.path.join(PASTA, "*FW*.xlsx")) + glob.glob(os.path.join(PASTA, "*FW *.xlsx"))
fw_files = list(set(fw_files))
print(f"\nArquivos de Performance encontrados: {len(fw_files)}")

for arquivo in fw_files:
    print(f"\nImportando: {arquivo}")
    try:
        df = pd.read_excel(arquivo, sheet_name=0, header=None)

        # Extrai período do cabeçalho
        periodo = str(df.iloc[0, 0]).replace("Date Range: ", "").strip()
        fw_nome = os.path.basename(arquivo).replace(".xlsx", "")
        periodo_completo = f"{fw_nome} | {periodo}"
        print(f"  Período: {periodo_completo}")

        # Lê dados a partir da linha 3 (índice 2 = cabeçalho, índice 3+ = dados)
        for i in range(3, len(df)):
            row = df.iloc[i]
            restaurant = str(row[0]).strip() if pd.notna(row[0]) else None
            if not restaurant or restaurant == "nan":
                continue
            try:
                cur.execute("""
                    INSERT INTO pesquisa_performance
                        (restaurant, country, count, overall_experience, overall_dissat,
                         value, service, taste, speed_of_service, clean,
                         soup_salad_refill, breadstick_refill, periodo, arquivo_origem)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (restaurant, periodo) DO NOTHING
                """, (
                    normalizar_filial(restaurant),
                    str(row[1]) if pd.notna(row[1]) else None,
                    int(row[2]) if pd.notna(row[2]) else None,
                    float(row[3]) if pd.notna(row[3]) else None,
                    float(row[4]) if pd.notna(row[4]) else None,
                    float(row[5]) if pd.notna(row[5]) else None,
                    float(row[6]) if pd.notna(row[6]) else None,
                    float(row[7]) if pd.notna(row[7]) else None,
                    float(row[8]) if pd.notna(row[8]) else None,
                    float(row[9]) if pd.notna(row[9]) else None,
                    float(row[10]) if pd.notna(row[10]) else None,
                    float(row[11]) if pd.notna(row[11]) else None,
                    periodo_completo,
                    os.path.basename(arquivo)
                ))
                if cur.rowcount > 0:
                    print(f"  ✅ {normalizar_filial(restaurant)}")
                else:
                    print(f"  ⚠️  Duplicata: {restaurant}")
            except Exception as e:
                conn.rollback()
                print(f"  Erro: {e}")
        conn.commit()
    except Exception as e:
        print(f"  Erro ao ler arquivo: {e}")

# Resumo final
cur.execute("SELECT COUNT(*) FROM pesquisa_comments")
print(f"\n✅ Total pesquisa_comments: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pesquisa_performance")
print(f"✅ Total pesquisa_performance: {cur.fetchone()[0]}")
cur.execute("SELECT DISTINCT arquivo_origem FROM pesquisa_comments")
print(f"\nArquivos importados (comments):")
for row in cur.fetchall():
    print(f"  {row[0]}")
cur.execute("SELECT DISTINCT arquivo_origem FROM pesquisa_performance")
print(f"\nArquivos importados (performance):")
for row in cur.fetchall():
    print(f"  {row[0]}")

cur.close()
conn.close()
print("\nImportação concluída!")