import psycopg2
from db import get_conn
import pandas as pd
import sys

print("=" * 50)
print("VALIDAÇÃO DOS DADOS — Olive Garden")
print("=" * 50)

conn = get_conn()
cur = conn.cursor()

erros = []
avisos = []

# 1. Total de reviews
cur.execute("SELECT COUNT(*) FROM reviews")
total = cur.fetchone()[0]
print(f"\n[1] Total de reviews: {total}")
if total < 150:
    erros.append(f"Total de reviews muito baixo: {total} (esperado >= 150)")
elif total < 180:
    avisos.append(f"Total de reviews abaixo do esperado: {total}")

# 2. Filiais corretas
FILIAIS_ESPERADAS = {
    "Olive Garden - Aricanduva",
    "Olive Garden - Center Norte",
    "Olive Garden - Dom Pedro",
    "Olive Garden - Guarulhos GRU2",
    "Olive Garden - Guarulhos GRU3",
    "Olive Garden - Morumbi",
}
cur.execute("SELECT DISTINCT filial FROM reviews ORDER BY filial")
filiais_banco = {row[0] for row in cur.fetchall()}
print(f"\n[2] Filiais no banco: {len(filiais_banco)}")
for f in sorted(filiais_banco):
    print(f"    {f}")

filiais_erradas = filiais_banco - FILIAIS_ESPERADAS
if filiais_erradas:
    erros.append(f"Filiais incorretas encontradas: {filiais_erradas}")

filiais_faltando = FILIAIS_ESPERADAS - filiais_banco
if filiais_faltando:
    avisos.append(f"Filiais faltando: {filiais_faltando}")

# 3. Google em português
cur.execute("SELECT texto FROM reviews WHERE plataforma = 'Google Reviews' LIMIT 30")
textos_google = [row[0] for row in cur.fetchall() if row[0]]
em_ingles = [t for t in textos_google if t and not any(c in t.lower() for c in ['ã', 'ç', 'é', 'ê', 'ó', 'ô', 'ú', 'á', 'à', 'í']) and len(t.split()) > 5]
print(f"\n[3] Google Reviews em inglês: {len(em_ingles)}/{len(textos_google)}")
if len(em_ingles) > 3:
    erros.append(f"Muitos reviews do Google em inglês: {len(em_ingles)}")
elif len(em_ingles) > 0:
    avisos.append(f"Alguns reviews do Google em inglês: {len(em_ingles)}")

# 4. Duplicatas
cur.execute("""
    SELECT COUNT(*) FROM (
        SELECT autor, texto, filial, COUNT(*)
        FROM reviews
        GROUP BY autor, texto, filial
        HAVING COUNT(*) > 1
    ) t
""")
duplicatas = cur.fetchone()[0]
print(f"\n[4] Duplicatas: {duplicatas}")
if duplicatas > 0:
    erros.append(f"Duplicatas encontradas: {duplicatas}")

# 5. Distribuição de sentimento
cur.execute("SELECT sentimento, COUNT(*) FROM reviews GROUP BY sentimento")
dist = {row[0]: row[1] for row in cur.fetchall()}
total_sent = sum(dist.values())
pct_pos = dist.get("Positivo", 0) / total_sent * 100 if total_sent > 0 else 0
pct_neg = dist.get("Negativo", 0) / total_sent * 100 if total_sent > 0 else 0
print(f"\n[5] Sentimento:")
for s, c in dist.items():
    print(f"    {s}: {c} ({c/total_sent*100:.1f}%)")
if pct_pos < 30:
    avisos.append(f"% Positivo muito baixo: {pct_pos:.1f}%")
if pct_neg > 70:
    avisos.append(f"% Negativo muito alto: {pct_neg:.1f}%")

# 6. Plataformas
cur.execute("SELECT plataforma, COUNT(*) FROM reviews GROUP BY plataforma")
print(f"\n[6] Por plataforma:")
for row in cur.fetchall():
    print(f"    {row[0]}: {row[1]}")

# 7. Notícias
cur.execute("SELECT COUNT(*) FROM noticias")
total_news = cur.fetchone()[0]
print(f"\n[7] Notícias: {total_news}")
if total_news < 10:
    avisos.append(f"Poucas notícias no banco: {total_news}")

# 8. Social
cur.execute("SELECT COUNT(*) FROM social")
total_social = cur.fetchone()[0]
print(f"\n[8] Social: {total_social}")

cur.close()
conn.close()

# Resultado final
print("\n" + "=" * 50)
if erros:
    print("❌ ERROS ENCONTRADOS — atualização bloqueada:")
    for e in erros:
        print(f"   • {e}")
    print("=" * 50)
    sys.exit(1)
elif avisos:
    print("⚠️  AVISOS — verifique antes de continuar:")
    for a in avisos:
        print(f"   • {a}")
    print("=" * 50)
    print("✅ Validação passou com avisos.")
else:
    print("✅ TUDO OK — dados validados com sucesso!")
    print("=" * 50)