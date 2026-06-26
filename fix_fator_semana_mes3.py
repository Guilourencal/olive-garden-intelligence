content = open('aprender_modelo.py', 'r', encoding='utf-8').read()

old = "        p_stl = m['media'] * m['fator_dow'].get(dow_d,1.0) * m['fator_mes'].get(mes_d,1.0) * m['fator_rec']"
new = "        sem_d = 1 if data_alvo.day<=7 else 2 if data_alvo.day<=14 else 3 if data_alvo.day<=21 else 4\n        f_sem = float(m['fator_semana_mes'].get(sem_d, 1.0))\n        p_stl = m['media'] * m['fator_dow'].get(dow_d,1.0) * m['fator_mes'].get(mes_d,1.0) * m['fator_rec'] * f_sem"

if old in content:
    content = content.replace(old, new)
    open('aprender_modelo.py', 'w', encoding='utf-8').write(content)
    print('OK p_stl')
else:
    print('TRECHO NAO ENCONTRADO')
