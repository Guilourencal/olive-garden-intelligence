lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'int(gc):,}'.replace' in line or '".replace(",",".")' in line and 'int(gc)' in line:
        lines[i] = '                    <div style="font-size:22px; font-weight:800;">{gc_fmt}</div></div>'
        print(f'Linha {i+1} corrigida!')
        break
# Adicionar gc_fmt antes dos cards
for i, line in enumerate(lines):
    if 'cor_ano12 = "#2e6b3e"' in line:
        lines.insert(i, '            gc_fmt = f"{int(gc):,}".replace(",",".")')
        print(f'gc_fmt inserido na linha {i+1}')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
