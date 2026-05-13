import pandas as pd

arquivo = "data/ifood_vendas/iFood_Vendas_Maio2026_06.xlsx"
df = pd.read_excel(arquivo, sheet_name='Vendas', header=0)
df.columns = ['periodo','marca','servico','logistica','id_loja','filial','estado','cidade','pedidos','faturamento','taxa_entrega','ticket_medio','novos_clientes']
print(df[['periodo','filial','logistica','pedidos','faturamento','ticket_medio']].to_string())
