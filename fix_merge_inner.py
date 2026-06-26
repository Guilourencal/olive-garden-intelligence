lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

lines[828] = '        cruzado = pd.merge(interno, externo[["filial", "score_externo"]], on="filial", how="inner")\n'
lines[829] = '        cruzado = cruzado.dropna(subset=["score_interno", "score_externo"])\n'
lines[830] = '        cruzado["filial_curta"] = cruzado["filial"].str.replace("Olive Garden - ", "")\n'

open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
