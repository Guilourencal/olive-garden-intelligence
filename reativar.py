lines = open('atualizar_tudo.py', 'r', encoding='utf-8').read().split('\n')
if lines[0] == 'import sys' and lines[1] == 'print("Pipeline pausado temporariamente.")':
    lines = lines[3:]
    open('atualizar_tudo.py', 'w', encoding='utf-8').write('\n'.join(lines))
    print('Pipeline reativado!')
else:
    print('Bloco de pausa nao encontrado na linha 1')
    print(f'Linha 0: {lines[0]}')
    print(f'Linha 1: {lines[1]}')
