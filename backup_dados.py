import psycopg2
import pandas as pd
from datetime import datetime
import os

print("=" * 50)
print("BACKUP DOS DADOS — Olive Garden")
print("=" * 50)

# Cria pasta de backup se não existir
os.makedirs("backups", exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)

tabelas = ["reviews", "social", "noticias"]

for tabela in tabelas:
    try:
        df = pd.read_sql(f"SELECT * FROM {tabela}", conn)
        arquivo = f"backups/{tabela}_{timestamp}.csv"
        df.to_csv(arquivo, index=False, encoding="utf-8-sig")
        print(f"✅ {tabela}: {len(df)} registros → {arquivo}")
    except Exception as e:
        print(f"❌ Erro ao fazer backup de {tabela}: {e}")

conn.close()
print(f"\nBackup concluído: {timestamp}")
print("=" * 50)