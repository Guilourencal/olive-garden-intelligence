lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

# Deletar Bloco 1 Radar (linhas 1800-1829, indices 1799-1828)
del lines[1799:1829]

# Renomear aba Correlacoes para Analises
for i, line in enumerate(lines):
    if 'Correlacoes' in line:
        lines[i] = lines[i].replace('Correlacoes', 'Analises')

open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print(f'OK — {len(lines)} linhas')
