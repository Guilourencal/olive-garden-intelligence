content = open('aprender_modelo.py', 'r', encoding='utf-8').read()

old = "    return {\n        'media': media, 'fator_dow': fator_dow, 'fator_mes': fator_mes,"
new = "    return {\n        'media': media, 'fator_dow': fator_dow, 'fator_mes': fator_mes, 'fator_semana_mes': fator_semana_mes,"

if old in content:
    content = content.replace(old, new)
    open('aprender_modelo.py', 'w', encoding='utf-8').write(content)
    print('OK retorno')
else:
    print('TRECHO NAO ENCONTRADO')
