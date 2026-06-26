lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
idx = next(i for i, l in enumerate(lines) if 'elif aba_sel == "OlivIA":' in l)
for i, line in enumerate(lines[idx:idx+30], idx+1):
    print(f'{i}: {repr(line[:90])}')
