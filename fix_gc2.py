lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
lines[1124] = '                    <div style="font-size:22px; font-weight:800;">{gc_fmt}</div></div>'
# Adicionar gc_fmt
for i, line in enumerate(lines):
    if 'cor_meta2 = ' in line:
        lines.insert(i, '            gc_fmt = str(int(gc)).replace("", "").replace("000", ".000") if gc > 0 else "0"')
        lines.insert(i, '            gc_fmt = f"{int(gc):,}".replace(",", ".")')
        del lines[i]
        print(f'gc_fmt adicionado na linha {i+1}')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
