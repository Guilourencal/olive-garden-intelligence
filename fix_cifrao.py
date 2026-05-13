content = open('dashboard.py', 'r', encoding='utf-8').read()
import re
content = content.replace('R', 'R&#36;{fat:,.0f}')
content = content.replace('R', 'R&#36;{tkt:.0f}')
content = content.replace('R', 'R&#36;{x:,.0f}')
open('dashboard.py', 'w', encoding='utf-8').write(content)
print('Feito!')
