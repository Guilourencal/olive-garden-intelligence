content = open('importar_ifood_tags.py', 'r', encoding='utf-8').read()
content = content.replace(
    'pct = round(sim / total * 100, 1) if total > 0 else 0',
    'pct = float(round(float(sim) / total * 100, 1)) if total > 0 else 0.0'
)
content = content.replace(
    '""", (periodo, filial, tag_label, tipo, int(sim), int(nao), pct, int(sim), int(nao), pct))',
    '""", (periodo, filial, tag_label, tipo, int(sim), int(nao), pct, int(sim), int(nao), pct))'
)
open('importar_ifood_tags.py', 'w', encoding='utf-8').write(content)
print('Feito!')
