lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
lines.insert(801, '    df_comments_f = df_comments[df_comments["filial"].notna() & (df_comments["filial"] != "nan")].copy()\n')
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
