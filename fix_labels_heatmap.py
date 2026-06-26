lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

# Deletar linha 900 duplicada (indice 900)
del lines[900]

# Inserir labels antes do pivot (agora linha 902, indice 901)
lines.insert(902, '            labels = ["Experiencia Geral", "Valor", "Atendimento", "Sabor", "Velocidade", "Limpeza", "Refil Sopa/Salada", "Refil Breadstick"]\n')

open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
