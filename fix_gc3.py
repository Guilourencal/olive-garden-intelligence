lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
# Remover linha errada 1097 (indice)
del lines[1097]
# Inserir gc_fmt antes do Card 1 (linha 1094 - antes do comentario)
for i, line in enumerate(lines):
    if '# Card 1 - Venda Total vs Budget' in line:
        lines.insert(i, '            gc_fmt = f"{int(gc):,}".replace(",", ".")')
        print(f'gc_fmt inserido na linha {i+1}')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
