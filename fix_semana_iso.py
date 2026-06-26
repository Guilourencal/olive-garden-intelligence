content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '''                # Mesma semana ano anterior
                seg_ano1 = ultima_seg - timedelta(days=364)
                dom_ano1 = ultimo_dom - timedelta(days=364)
                df_ano1 = df_dow_base[(df_dow_base["data_dt"] >= seg_ano1) & (df_dow_base["data_dt"] <= dom_ano1)]
                sem_label = f"{ultima_seg.strftime('%d/%m')} - {ultimo_dom.strftime('%d/%m/%Y')}"'''

new = '''                # Numero da semana ISO da ultima semana fechada
                num_semana = int(ultima_seg.isocalendar()[1])
                ano_atual = int(ultima_seg.year)
                ano_anterior = ano_atual - 1
                # Mesma semana ISO no ano anterior
                df_dow_base["iso_week"] = df_dow_base["data_dt"].dt.isocalendar().week.astype(int)
                df_dow_base["iso_year"] = df_dow_base["data_dt"].dt.isocalendar().year.astype(int)
                df_ano1 = df_dow_base[(df_dow_base["iso_week"] == num_semana) & (df_dow_base["iso_year"] == ano_anterior)]
                sem_label = f"Sem. {num_semana}/{ano_atual} ({ultima_seg.strftime('%d/%m')} - {ultimo_dom.strftime('%d/%m')}) vs Sem. {num_semana}/{ano_anterior}"'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
