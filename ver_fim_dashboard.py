lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
print(f'Total linhas: {len(lines)}')
for i, line in enumerate(lines[-20:], len(lines)-19):
    print(f'{i}: {line}', end='')
