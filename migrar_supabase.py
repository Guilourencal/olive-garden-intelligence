import psycopg2
import pandas as pd

LOCAL = {
    "host": "127.0.0.1",
    "port": 5432,
    "user": "postgres",
    "password": "olivegarden2233@",
    "database": "olive_garden"
}

SUPABASE = {
    "host": "aws-1-sa-east-1.pooler.supabase.com",
    "port": 6543,
    "user": "postgres.rvauallshhozpruvusrr",
    "password": "olivegarden2233@",
    "database": "postgres"
} 

print("Lendo dados do banco local...")
conn_local = psycopg2.connect(**LOCAL)
cur_local = conn_local.cursor()
cur_local.execute("SELECT * FROM reviews")
rows = cur_local.fetchall()
cols = [desc[0] for desc in cur_local.description]
df = pd.DataFrame(rows, columns=cols)
print(f"  {len(df)} reviews encontrados")
cur_local.close()
conn_local.close()

print("Conectando ao Supabase...")
conn_supa = psycopg2.connect(**SUPABASE)
cur_supa = conn_supa.cursor()

print("Criando tabela no Supabase...")
cur_supa.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id SERIAL PRIMARY KEY,
        filial VARCHAR(255),
        plataforma VARCHAR(100),
        autor VARCHAR(255),
        nota FLOAT,
        texto TEXT,
        data_original VARCHAR(100),
        data_coleta VARCHAR(50),
        nota_geral_filial FLOAT,
        total_avaliacoes_filial FLOAT,
        sentimento VARCHAR(50),
        sentimento_score FLOAT,
        tema VARCHAR(255),
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(autor, texto, filial)
    )
""")
conn_supa.commit()
print("  Tabela criada!")

print("Migrando dados...")
inseridos = 0
for _, row in df.iterrows():
    try:
        cur_supa.execute("""
            INSERT INTO reviews (filial, plataforma, autor, nota, texto,
                data_original, data_coleta, nota_geral_filial,
                total_avaliacoes_filial, sentimento, sentimento_score, tema)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (autor, texto, filial) DO NOTHING
        """, (
            row.get("filial"), row.get("plataforma"), row.get("autor"),
            row.get("nota"), row.get("texto"), row.get("data_original"),
            row.get("data_coleta"), row.get("nota_geral_filial"),
            row.get("total_avaliacoes_filial"), row.get("sentimento"),
            row.get("sentimento_score"), row.get("tema")
        ))
        inseridos += 1
    except Exception as e:
        conn_supa.rollback()
        print(f"  Erro: {e}")

conn_supa.commit()
print(f"  {inseridos} reviews migrados!")

cur_supa.execute("SELECT COUNT(*) FROM reviews")
print(f"\nTotal no Supabase: {cur_supa.fetchone()[0]}")

cur_supa.close()
conn_supa.close()
print("\nMigração concluída!")