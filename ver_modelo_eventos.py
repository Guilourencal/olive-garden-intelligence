lines = open('aprender_modelo.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'calendario' in line.lower() or 'evento' in line.lower() or 'feriado' in line.lower():
        print(f'{i+1}: {line}', end='')
