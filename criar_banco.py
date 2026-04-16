import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd

DB_PASSWORD = "olivegarden2233@"
DB_USER = "postgres"
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_NAME = "olive_garden"

def get_conn(database="postgres"):
    return psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=database)

conn = get_conn()
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
if not cur.fetchone():
    cur.execute(f"CREATE DATABASE {DB_NAME}")
    print("Banco criado!")
else:
    print("Banco ja existe.")
cur.close()
conn.close()

conn = get_conn(DB_NAME)
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS reviews")
conn.commit()
cur.execute("""
    CREATE TABLE reviews (
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
conn.commit()
print("Tabela criada!")

df = pd.read_csv("reviews_classificado.csv", encoding="utf-8-sig")
df = df.where(pd.notnull(df), None)
inseridos = 0

for _, row in df.iterrows():
    try:
        cur.execute("""
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
        conn.rollback()
        print(f"Erro: {e}")

conn.commit()
print(f"Inseridos: {inseridos}")

cur.execute("SELECT COUNT(*) FROM reviews")
print(f"Total no banco: {cur.fetchone()[0]}")

cur.execute("""
    SELECT plataforma, sentimento, COUNT(*)
    FROM reviews GROUP BY plataforma, sentimento ORDER BY plataforma
""")
print("\nResumo:")
for row in cur.fetchall():
    print(f"  {row[0]} | {row[1]} | {row[2]}")

cur.close()
conn.close()