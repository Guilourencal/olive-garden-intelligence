lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

# Corrigir ordenacao do periodo_curto — extrair numero do FW para ordenar corretamente
lines[896] = '            df_perf_f["periodo_curto"] = df_perf_f["periodo"].str.extract(r"(FW\d+ to FW\d+)")\n'
lines[897] = '            df_perf_f["fw_num"] = df_perf_f["periodo_curto"].str.extract(r"FW(\d+)").astype(float)\n'
lines[898] = '            ultimo_periodo = df_perf_f.loc[df_perf_f["fw_num"].idxmax(), "periodo_curto"] if len(df_perf_f) > 0 else ""\n'
lines[899] = '            df_perf_f = df_perf_f[df_perf_f["periodo_curto"] == ultimo_periodo]\n'

open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
