lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

lines[1307] = '            _hoje = df_vd["data"].max()\n'
lines[1308] = '            if len(df_vd_f) > 0:\n'
lines[1309] = '                df_mes_hdc = df_vd_f.copy()\n'
lines[1310] = '            else:\n'
lines[1311] = '                df_mes_hdc = df_vd[\n'
lines[1312] = '                    (df_vd["data"].dt.month == _hoje.month) &\n'
lines[1313] = '                    (df_vd["data"].dt.year == _hoje.year) &\n'
lines.insert(1314, '                    df_vd["filial_curta"].isin(filiais_sel)\n')
lines.insert(1315, '                ].copy()\n')
del lines[1316]

open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
