lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

# Inserir regras SQL antes da linha 1733 (fechamento do system prompt)
regras_sql = '''Regras SQL importantes para PostgreSQL/Supabase:
- Use ROUND(valor::numeric, 2) para arredondamento — NUNCA ROUND(double_precision, integer)
- Para percentuais: ROUND((a::numeric / NULLIF(b::numeric,0)) * 100, 1)
- Datas: EXTRACT(year FROM data), EXTRACT(month FROM data)
- Filiais sempre com nome completo: "Olive Garden - Morumbi" etc
- Para YTD 2026: WHERE EXTRACT(year FROM data) = 2026
- Para mes corrente: WHERE EXTRACT(month FROM data) = 6 AND EXTRACT(year FROM data) = 2026
- Sempre use aliases claros nas colunas (AS faturamento_total, etc)
- Limite resultados com LIMIT 50 quando nao for agregacao

'''

lines.insert(1732, regras_sql)
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
