lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'periodo_tag_sel = st.selectbox("Periodo:", periodos_tags' in line:
        lines[i] = '            col_sel1, col_sel2 = st.columns(2)'
        lines.insert(i+1, '            with col_sel1:')
        lines.insert(i+2, '                periodo_tag_sel = st.selectbox("Periodo:", periodos_tags, index=len(periodos_tags)-1, key="periodo_tags")')
        lines.insert(i+3, '            with col_sel2:')
        lines.insert(i+4, '                filiais_tags = ["Todas"] + sorted(df_ifood_tags["filial"].str.replace("Olive Garden - ", "", regex=False).unique().tolist())')
        lines.insert(i+5, '                filial_tag_sel = st.selectbox("Filial:", filiais_tags, key="filial_tags")')
        lines.insert(i+6, '            df_tags_f = df_ifood_tags[df_ifood_tags["periodo"] == periodo_tag_sel]')
        lines.insert(i+7, '            if filial_tag_sel != "Todas":')
        lines.insert(i+8, '                df_tags_f = df_tags_f[df_tags_f["filial"].str.contains(filial_tag_sel, regex=False)]')
        print(f'Linha {i+1} atualizada!')
        break

# Remover linha antiga de df_tags_f
for i, line in enumerate(lines):
    if 'df_tags_f = df_ifood_tags[df_ifood_tags["periodo"] == periodo_tag_sel]' in line and i > 535:
        del lines[i]
        print(f'Linha duplicada removida!')
        break

open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
