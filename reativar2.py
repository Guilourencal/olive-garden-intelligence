lines = open('atualizar_tudo.py', 'r', encoding='utf-8').read().split('\n')
if 'pausado' in lines[1]:
    lines = lines[3:]
    open('atualizar_tudo.py', 'w', encoding='utf-8').write('\n'.join(lines))
    print('Pipeline reativado!')
else:
    print(f'Linha 1: {lines[1]}')
