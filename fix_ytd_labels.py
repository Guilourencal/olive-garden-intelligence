content = open('dashboard.py', 'r', encoding='utf-8').read()

old = "'FATURAMENTO TOTAL MTD'"
new = "'FATURAMENTO TOTAL YTD'"

old2 = "'IFOOD MTD'"
new2 = "'IFOOD YTD'"

c1 = content.count(old)
c2 = content.count(old2)
content = content.replace(old, new).replace(old2, new2)
open('dashboard.py', 'w', encoding='utf-8').write(content)
print(f'OK — {c1} label faturamento + {c2} label ifood atualizados')
