lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
# Remover linha solta 1194 (indice 1194)
if 'textposition="inside",' in lines[1194] and 'fig_dias' in lines[1195]:
    del lines[1194]
    print('Linha removida!')
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
