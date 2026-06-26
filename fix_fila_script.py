content = open('importar_fila_espera.py', 'r', encoding='utf-8').read()

old = "            cur.execute(\"\"\"\n                INSERT INTO fila_espera\n                (registro_id, nome, pessoas, dia_chegada, hora_chegada, dia_finalizada, hora_finalizada, duracao_minutos, status, origem, unidade, arquivo_origem)\n                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\n                ON CONFLICT (registro_id) DO NOTHING\n            \"\"\", (reg_id, nome, pessoas, dia_ch, hora_ch, dia_fin, hora_fin, duracao, 'Restaurant', unidade, arquivo))"
new = "            cur.execute(\"\"\"\n                INSERT INTO fila_espera\n                (registro_id, nome, pessoas, dia_chegada, hora_chegada, dia_finalizada, hora_finalizada, duracao_minutos, status, origem, unidade, arquivo_origem)\n                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\n                ON CONFLICT (registro_id) DO NOTHING\n            \"\"\", (reg_id, nome, pessoas, dia_ch, hora_ch, dia_fin, hora_fin, duracao, status, 'Restaurant', unidade, arquivo))"

if old in content:
    content = content.replace(old, new)
    open('importar_fila_espera.py', 'w', encoding='utf-8').write(content)
    print('OK script corrigido')
else:
    print('TRECHO NAO ENCONTRADO')
