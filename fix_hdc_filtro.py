content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '            _hoje = df_vd["data"].max()\n            df_mes_hdc = df_vd[\n                (df_vd["data"].dt.month == _hoje.month) &\n                (df_vd["data"].dt.year == _hoje.year) &\n                df_vd["filial_curta"].isin(filiais_sel)\n            ].copy()'
new = '            _hoje = df_vd["data"].max()\n            if len(df_vd_f) > 0:\n                df_mes_hdc = df_vd_f.copy()\n            else:\n                df_mes_hdc = df_vd[\n                    (df_vd["data"].dt.month == _hoje.month) &\n                    (df_vd["data"].dt.year == _hoje.year) &\n                    df_vd["filial_curta"].isin(filiais_sel)\n                ].copy()'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
