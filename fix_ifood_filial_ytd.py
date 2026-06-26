content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '                if meses_num_sel and len(meses_num_sel) < 12:\n                    df_if_ytd = df_if_ytd[df_if_ytd["periodo"].str[3:5].isin(meses_num_sel)]\n            else:\n                df_if_ytd = pd.DataFrame()\n            fat_if_ytd = df_if_ytd["faturamento"].sum() if len(df_if_ytd) > 0 else 0'

new = '                if meses_num_sel and len(meses_num_sel) < 12:\n                    df_if_ytd = df_if_ytd[df_if_ytd["periodo"].str[3:5].isin(meses_num_sel)]\n                # Filtrar por filial\n                filiais_ifood_full = ["Olive Garden - " + f for f in filiais_sel if f in ["Morumbi","Center Norte","Dom Pedro","Aricanduva"]]\n                if filiais_ifood_full:\n                    df_if_ytd = df_if_ytd[df_if_ytd["filial"].isin(filiais_ifood_full)]\n                else:\n                    df_if_ytd = pd.DataFrame()\n            else:\n                df_if_ytd = pd.DataFrame()\n            fat_if_ytd = df_if_ytd["faturamento"].sum() if len(df_if_ytd) > 0 else 0'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
