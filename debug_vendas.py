import pandas as pd
import glob
import os

arquivos = glob.glob("data/ifood_vendas/iFood_Vendas_*.xlsx")
for arquivo in arquivos:
    nome = os.path.basename(arquivo)
    print(f"\n=== {nome} ===")
    df = pd.read_excel(arquivo, sheet_name='Vendas', header=0)
    df.columns = ['periodo','marca','servico','logistica','id_loja','filial','estado','cidade','pedidos','faturamento','taxa_entrega','ticket_medio','novos_clientes']
    print(df[['filial','logistica','pedidos','faturamento','ticket_medio','novos_clientes']].to_string())
    print(f"\nTipos: {df[['pedidos','faturamento','ticket_medio']].dtypes.to_string()}")
