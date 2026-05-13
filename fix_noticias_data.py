lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'data_corte = (datetime.now() - timedelta(days=dias_sel)).strftime' in line:
        lines[i] = '    data_corte = (datetime.now() - timedelta(days=dias_sel)).strftime("%Y-%m-%d")'
        print(f'Linha {i+1} encontrada')
    if 'df_news_f = df_news_f[df_news_f["publicado_em"] >= data_corte]' in line:
        lines[i] = '    df_news_f = df_news_f[pd.to_datetime(df_news_f["publicado_em"], errors="coerce", utc=True) >= pd.Timestamp(data_corte, tz="UTC")]'
        print(f'Linha {i+1} corrigida!')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
