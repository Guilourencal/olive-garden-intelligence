content = open('atualizar_tudo.py', 'r', encoding='utf-8').read()
new_content = 'import sys\nprint("Pipeline pausado temporariamente.")\nsys.exit(0)\n' + content
open('atualizar_tudo.py', 'w', encoding='utf-8').write(new_content)
print('Feito!')
