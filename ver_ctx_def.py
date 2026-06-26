lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if '_gerar_contexto_banco' in line or '_contexto_dinamico = ' in line:
        print(f'{i+1}: {repr(line[:100])}')
