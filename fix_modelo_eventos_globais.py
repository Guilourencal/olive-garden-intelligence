content = open('aprender_modelo.py', 'r', encoding='utf-8').read()

old = '''    fil_curta = fil_ev.replace("Olive Garden - ", "") if fil_ev else None
    d = d_ini
    while d <= d_fim:
        if fil_curta:
            eventos_por_filial.setdefault(fil_curta, set()).add(d)
        d = _date(d.year, d.month, d.day + 1) if d.day < 28 else (_date(d.year, d.month+1, 1) if d.month < 12 else _date(d.year+1, 1, 1))'''

new = '''    fil_curta = fil_ev.replace("Olive Garden - ", "") if fil_ev else None
    d = d_ini
    while d <= d_fim:
        if fil_curta:
            eventos_por_filial.setdefault(fil_curta, set()).add(d)
        else:
            for _f in ['Aricanduva','Center Norte','Dom Pedro','Guarulhos GRU2','Guarulhos GRU3','Morumbi']:
                eventos_por_filial.setdefault(_f, set()).add(d)
        d = _date(d.year, d.month, d.day + 1) if d.day < 28 else (_date(d.year, d.month+1, 1) if d.month < 12 else _date(d.year+1, 1, 1))'''

if old in content:
    content = content.replace(old, new)
    open('aprender_modelo.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
