import psycopg2

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)
cur = conn.cursor()

# Remove duplicatas
cur.execute("""
    DELETE FROM reviews
    WHERE filial = 'Olive Garden - Campinas'
    AND (autor, texto) IN (
        SELECT autor, texto FROM reviews
        WHERE filial = 'Olive Garden - Dom Pedro'
    )
""")
print(f"Duplicatas removidas: {cur.rowcount}")
conn.commit()

cur.execute("UPDATE reviews SET filial = 'Olive Garden - Guarulhos GRU2' WHERE filial = 'Olive Garden - GRU2'")
cur.execute("UPDATE reviews SET filial = 'Olive Garden - Guarulhos GRU3' WHERE filial = 'Olive Garden - GRU3'")
cur.execute("UPDATE reviews SET filial = 'Olive Garden - Dom Pedro' WHERE filial = 'Olive Garden - Campinas'")
conn.commit()
print("Filiais corrigidas!")

cur.execute("SELECT DISTINCT filial FROM reviews ORDER BY filial")
print("\nFiliais atuais:")
for row in cur.fetchall():
    print(f"  {row[0]}")

cur.execute("SELECT COUNT(*) FROM reviews")
print(f"\nTotal: {cur.fetchone()[0]}")

cur.close()
conn.close()