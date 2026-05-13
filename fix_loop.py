with open('dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '    for aba in ["Reviews", "Social", "Notícias", "Pesquisa", "Vendas", "Insights IA"]:'
new = '    for aba in ["Reviews", "Social", "Pesquisa", "Vendas", "OlivIA"]:'
content = content.replace(old, new)

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')
