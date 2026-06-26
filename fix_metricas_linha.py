lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
lines[900] = '            df_perf_f = df_perf_f[df_perf_f["periodo_curto"] == ultimo_periodo]\n'
lines.insert(901, '            metricas = ["overall_experience", "value", "service", "taste", "speed_of_service", "clean", "soup_salad_refill", "breadstick_refill"]\n')
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
