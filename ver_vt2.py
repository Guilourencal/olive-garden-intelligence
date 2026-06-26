lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'vt =' in line or 'vt=' in line or 'venda_total' in line or 'df_vd_f' in line:
        if 950 <= i+1 <= 1010:
            print(f'{i+1}: {line}', end='')
