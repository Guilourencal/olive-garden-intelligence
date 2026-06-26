content = open('dashboard.py', 'r', encoding='utf-8').read()

old = "sem_label = f\"Sem. {num_semana}/{ano_atual} ({ultima_seg.strftime('%d/%m')} - {ultimo_dom.strftime('%d/%m')}) vs Sem. {num_semana}/{ano_anterior}\""
new = "sem_label = f\"Sem. {num_semana}/{ano_atual} vs Sem. {num_semana}/{ano_anterior}\""

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK titulo')
else:
    print('TRECHO NAO ENCONTRADO')
