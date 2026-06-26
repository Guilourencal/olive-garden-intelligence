lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

# Fix 1 — Label Faturamento Total MTD -> YTD
lines[1173] = lines[1173].replace('FATURAMENTO TOTAL MTD', 'FATURAMENTO TOTAL YTD')

# Fix 2 — Adicionar VS Budget e VS AA no box Faturamento Total
# Linha 1177 tem o % iFood — vamos expandir para incluir comparativos
lines[1176] = lines[1176].replace(
    '<div style="border-top:1px solid rgba(255,255,255,0.12);padding-top:8px;font-siz',
    '<div style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:10px;color:#9DC88D;"><span>VS Budget: <b style=\\"color:{cor_m2}\\">{seta_m2} {pct_meta:+.1f}%</b></span><span>VS AA: <b style=\\"color:{cor_a2}\\">{seta_a2} {pct_ano1:+.1f}%</b></span></div><div style="border-top:1px solid rgba(255,255,255,0.12);padding-top:8px;font-siz'
)

# Fix 3 — Label iFood MTD -> YTD
lines[1210] = lines[1210].replace('IFOOD MTD', 'IFOOD YTD')

open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
