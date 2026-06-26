lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
lines[464] = '            ranking["indice"] = (((ranking["nota_media"] - 1) / 4) * 40 + ranking["pct_pos"] * 0.6).clip(0, 100).round(0).fillna(0).astype(int)\n'
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
