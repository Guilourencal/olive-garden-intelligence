content = open('importar_ifood_reviews.py', 'r', encoding='utf-8').read()
old = '''            cur.execute("""
                INSERT INTO reviews (filial, plataforma, nota, texto, data_coleta, fonte_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (fonte_id) DO NOTHING
            """, (filial, 'iFood', nota, texto, datetime.now().strftime('%Y-%m-%d %H:%M'), id_pedido))
            
            if cur.rowcount > 0:
                ins += 1
            else:
                dup += 1'''
new = '''            cur.execute("SELECT id FROM reviews WHERE fonte_id = %s", (id_pedido,))
            if cur.fetchone():
                dup += 1
                continue
            cur.execute("""
                INSERT INTO reviews (filial, plataforma, nota, texto, data_coleta, fonte_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (filial, 'iFood', nota, texto, datetime.now().strftime('%Y-%m-%d %H:%M'), id_pedido))
            ins += 1'''
if old in content:
    content = content.replace(old, new)
    open('importar_ifood_reviews.py', 'w', encoding='utf-8').write(content)
    print('Feito!')
else:
    print('Trecho nao encontrado')
