lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
result = lines[:871] + lines[878:]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(result))
print('Feito! Linhas:', len(result))
