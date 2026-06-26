content = open('dashboard.py', 'r', encoding='utf-8').read()

old = 'for aba in ["Reviews", "Social", "Pesquisa", "Analises", "Vendas", "OlivIA", "Menu"]:'
new = 'for aba in ["Reviews", "Social", "Pesquisa", "Analises", "Vendas", "OlivIA", "Menu", "Fila"]:'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK aba')
else:
    print('TRECHO NAO ENCONTRADO')
