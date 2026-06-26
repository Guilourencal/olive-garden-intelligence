content = open('importar_fila_espera.py', 'r', encoding='utf-8').read()

old = '''            hora_ch = pd.to_datetime(str(row.get('Hora Chegada','')), format='%H:%M', errors='coerce').time() if pd.notna(row.get('Hora Chegada')) else None
            hora_fin = pd.to_datetime(str(row.get('Hora Finalizada','')), format='%H:%M', errors='coerce').time() if pd.notna(row.get('Hora Finalizada')) else None'''

new = '''            hora_ch_raw = row.get('Hora Chegada')
            hora_fin_raw = row.get('Hora Finalizada')
            hora_ch = pd.to_datetime(str(hora_ch_raw), format='%H:%M', errors='coerce').time() if pd.notna(hora_ch_raw) else None
            hora_fin = pd.to_datetime(str(hora_fin_raw), format='%H:%M', errors='coerce').time() if pd.notna(hora_fin_raw) else None'''

if old in content:
    content = content.replace(old, new)
    open('importar_fila_espera.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
