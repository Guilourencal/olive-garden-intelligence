lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
lines[2172] = '            df_scatter = pd.concat([df_mf[df_mf["type"]==t].nlargest(10, "revenue_score") for t in ["Star","Dog","Puzzle","Horse"] if len(df_mf[df_mf["type"]==t])>0]).reset_index(drop=True)\n'
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
