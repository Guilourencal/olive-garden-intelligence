lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'FATURAMENTO TOTAL' in line or 'IFOOD MTD' in line or 'IFOOD YTD' in line:
        print(f'{i+1}: {line}', end='')
