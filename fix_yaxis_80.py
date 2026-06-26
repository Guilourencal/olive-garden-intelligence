content = open('dashboard.py', 'r', encoding='utf-8').read()

old1 = 'yaxis=dict(title="% Topbox", range=[80, 100]'
new1 = 'yaxis=dict(title="% Topbox", range=[80, 101]'

old2 = 'yaxis=dict(range=[80, 100]'
new2 = 'yaxis=dict(range=[80, 101]'

count = content.count(old1) + content.count(old2)
content = content.replace(old1, new1).replace(old2, new2)
open('dashboard.py', 'w', encoding='utf-8').write(content)
print(f'OK — {count} ocorrencias substituidas')
