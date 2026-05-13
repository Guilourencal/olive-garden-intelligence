lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'sem_ano1 = sorted(semanas)[-53]' in line:
        # Corrigir logica de semana - ultima seg a dom fechada
        novo_bloco = [
            '                # Ultima semana fechada (seg a dom)',
            '                from datetime import timedelta',
            '                df_dow_base["data_dt"] = pd.to_datetime(df_dow_base["data"])',
            '                hoje_dt = df_dow_base["data_dt"].max()',
            '                # Encontrar o ultimo domingo fechado',
            '                dias_desde_dom = (hoje_dt.weekday() + 1) % 7',
            '                ultimo_dom = hoje_dt - timedelta(days=dias_desde_dom)',
            '                ultima_seg = ultimo_dom - timedelta(days=6)',
            '                df_ult = df_dow_base[(df_dow_base["data_dt"] >= ultima_seg) & (df_dow_base["data_dt"] <= ultimo_dom)]',
            '                # Mesma semana ano anterior',
            '                seg_ano1 = ultima_seg - timedelta(days=364)',
            '                dom_ano1 = ultimo_dom - timedelta(days=364)',
            '                df_ano1 = df_dow_base[(df_dow_base["data_dt"] >= seg_ano1) & (df_dow_base["data_dt"] <= dom_ano1)]',
            '                sem_label = f"{ultima_seg.strftime(\'%d/%m\')} - {ultimo_dom.strftime(\'%d/%m/%Y\')}"',
        ]
        # Encontrar inicio do bloco a substituir
        start = i - 3
        end = i + 2
        result_lines = lines[:start] + novo_bloco + lines[end:]
        open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(result_lines))
        print(f'Logica de semana corrigida!')
        break
