content = open('unificar_dados.py', 'r', encoding='utf-8').read()
old = '        if tags_pos: texto += f" [Tags positivas: {\', \'.join(tags_pos)}]"'
new = '        if tags_pos: texto += f" [Tags positivas: {\', \'.join(tags_pos)}] [ID:{id_pedido[:8]}]"'
if old in content:
    content = content.replace(old, new)
    open('unificar_dados.py', 'w', encoding='utf-8').write(content)
    print('Feito!')
else:
    print('Trecho nao encontrado - adicionando ID em todos os textos')
    content = content.replace(
        'ifood_rows.append({"filial": filial, "plataforma": "iFood", "nota": nota, "texto": texto, "autor": "", "data_original": data_av, "data_coleta": data_av})',
        'texto = f"{texto} [PID:{id_pedido[:8]}]"\n        ifood_rows.append({"filial": filial, "plataforma": "iFood", "nota": nota, "texto": texto, "autor": "", "data_original": data_av, "data_coleta": data_av})'
    )
    open('unificar_dados.py', 'w', encoding='utf-8').write(content)
    print('Feito com alternativa!')
