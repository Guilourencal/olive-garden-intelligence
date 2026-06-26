lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
idx = next(i for i, l in enumerate(lines) if 'elif aba_sel == "OlivIA":' in l)
print(f'OlivIA na linha: {idx+1}')
for i, line in enumerate(lines[idx:idx+15], idx+1):
    print(f'{i}: {repr(line[:80])}')
