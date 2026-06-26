lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

lines[1806] = '                                        {"role": "user", "content": "Aqui estao os dados retornados pelo banco:\\n\\n" + tabela + "\\nAgora apresente a analise executiva completa com a tabela e insights."}\n'
del lines[1807]
del lines[1807]
del lines[1807]
del lines[1807]

open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
