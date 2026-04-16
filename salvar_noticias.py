import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)
cur = conn.cursor()

# Limpa tudo
cur.execute("DELETE FROM noticias")
print(f"Notícias removidas: {cur.rowcount}")
conn.commit()

# Insere apenas as novas
df = pd.read_csv("noticias_bruto.csv", encoding="utf-8-sig")
df = df.where(pd.notnull(df), None)
inseridos = 0

for _, row in df.iterrows():
    try:
        cur.execute("""
            INSERT INTO noticias (categoria, titulo, descricao, fonte, url, imagem, publicado_em, data_coleta)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
        """, (
            row.get("categoria"), row.get("titulo"), row.get("descricao"),
            row.get("fonte"), row.get("url"), row.get("imagem"),
            row.get("publicado_em"), row.get("data_coleta")
        ))
        inseridos += 1
    except Exception as e:
        conn.rollback()
        print(f"Erro: {e}")

conn.commit()
cur.execute("SELECT COUNT(*) FROM noticias")
print(f"Total no banco: {cur.fetchone()[0]}")
cur.execute("SELECT categoria, COUNT(*) FROM noticias GROUP BY categoria")
print("\nPor categoria:")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")
cur.close()
conn.close()
print("\nConcluído!")