content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '                        fat_if_fil = df_v[df_v["periodo"]==p][df_v["filial"]==filial_full]["faturamento"].sum() if "filial" in df_v.columns else 0\n                            salao_fil = venda_salao_mes[venda_salao_mes["mes_ano"]==mes_ano_key]\n                            salao_fil_v = df_vd_share[df_vd_share["mes_ano"]==mes_ano_key & df_vd_share["filial"].str.contains(filial_if)]["venda_salao"].sum() if len(salao_fil)>0 else 0'
new = '                        fat_if_fil = df_v[(df_v["periodo"]==p) & (df_v["filial"]==filial_full)]["faturamento"].sum() if "filial" in df_v.columns else 0\n                            salao_fil_v = df_vd_share[(df_vd_share["mes_ano"]==mes_ano_key) & (df_vd_share["filial"].str.contains(filial_if, na=False))]["venda_salao"].sum()'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO — buscando linha exata')
    for i, line in enumerate(content.split('\n')):
        if 'fat_if_fil' in line or 'salao_fil' in line:
            if 1470 <= i+1 <= 1530:
                print(f'{i+1}: {repr(line)}')
