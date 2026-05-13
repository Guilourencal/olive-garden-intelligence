lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
lines[537] = '            df_tags_f = df_ifood_tags[df_ifood_tags["periodo"] == periodo_tag_sel]'
lines[538] = '            if filial_tag_sel != "Todas":'
lines[539] = '                df_tags_f = df_tags_f[df_tags_f["filial"].str.contains(filial_tag_sel, regex=False)]'
del lines[540]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('Feito!')
