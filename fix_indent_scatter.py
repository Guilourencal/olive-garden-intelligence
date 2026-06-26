lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
lines[2172] = '            df_scatter = df_scatter.sort_values("revenue_score", ascending=False).head(10)\n'
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
