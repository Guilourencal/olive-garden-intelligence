content = open('unificar_dados.py', 'r', encoding='utf-8').read()
old = "        if not texto.strip(): texto = f\"Avaliacao {nota} estrelas\""
new = "        if not texto.strip(): texto = f\"Avaliacao {nota} estrelas [ID:{id_pedido[:8]}]\""
content = content.replace(old, new)
open('unificar_dados.py', 'w', encoding='utf-8').write(content)
print('Feito!')
