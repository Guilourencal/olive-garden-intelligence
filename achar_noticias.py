lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if '"Reviews", "Social", "Noticias"' in line or 'Noticias' in line and 'btn_' in line or '"Notícias"' in line and 'for aba' in line:
        print(f'Linha {i+1}: {line}')
