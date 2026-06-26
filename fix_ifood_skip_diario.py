lines = open('importar_ifood_vendas.py', 'r', encoding='utf-8').readlines()
# Inserir verificacao de arquivo diario antes do print na linha 98
lines.insert(97, '''    # Ignorar arquivos diarios (periodo de 1 dia)
    try:
        df_test = pd.read_excel(caminho, sheet_name="Vendas", nrows=1)
        periodo_test = str(df_test["Período"].iloc[0])
        partes_test = periodo_test.split("-")
        if len(partes_test) == 2 and partes_test[0].strip() == partes_test[1].strip():
            print(f"  Ignorando arquivo diario: {nome}")
            continue
    except:
        pass
''')
open('importar_ifood_vendas.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
