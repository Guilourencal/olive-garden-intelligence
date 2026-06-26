content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '            # Usar periodo mais recente (mes corrente)\n            periodo_mes_atual = periodos[-1] if periodos else periodo_sel_v'
new = '            # Usar periodo mais recente (mes corrente) — ordenar por data\n            from datetime import datetime as _dt\n            def _parse_per(p):\n                try: return _dt.strptime(p.split("-")[1].strip(), "%d/%m/%Y")\n                except: return _dt(2000,1,1)\n            periodo_mes_atual = max(periodos, key=_parse_per) if periodos else periodo_sel_v'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
