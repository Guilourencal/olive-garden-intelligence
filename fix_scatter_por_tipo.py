lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
lines[2172] = '            df_scatter = df_scatter.groupby("type", group_keys=False).apply(lambda x: x.nlargest(10, "revenue_score")).reset_index(drop=True)\n'
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
