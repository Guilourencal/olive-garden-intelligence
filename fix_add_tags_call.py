lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'df_ifood_dias = carregar_ifood_dias()' in line:
        lines.insert(i + 1, 'df_ifood_tags = carregar_ifood_tags()')
        print(f'Call inserida na linha {i+2}')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
