content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '    rep_pub = df.groupby("filial").agg(nota_media=("nota", "mean"), pct_pos=("sentimento", lambda x: (x == "Positivo").sum() / len(x) * 100)).reset_index()'
new = '    df_rep = df[df["sentimento"].isin(["Positivo","Negativo","Neutro"])].copy()\n    rep_pub = df_rep.groupby("filial").agg(nota_media=("nota", "mean"), pct_pos=("sentimento", lambda x: (x == "Positivo").sum() / len(x) * 100)).reset_index()'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
