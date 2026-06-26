lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

# Adicionar regras de join apos linha 1740
novas_regras = '''- Para cruzar vendas_diarias com ifood_vendas, use EXTRACT(month FROM data) para o mes de vendas_diarias e extraia o mes do campo periodo de ifood_vendas com EXTRACT(month FROM TO_DATE(SPLIT_PART(periodo, \' - \', 1), \'DD/MM/YYYY\'))
- O campo mes em vendas_diarias e VARCHAR (ex: "jan", "fev") — nunca faca join direto com numeros
- Para cruzar por mes/ano entre tabelas, sempre use EXTRACT nas datas
- Exemplo de join correto entre vendas e ifood:
  SELECT EXTRACT(month FROM v.data) as mes_num, SUM(v.venda_salao) as salao, SUM(i.faturamento) as ifood
  FROM vendas_diarias v
  LEFT JOIN ifood_vendas i ON EXTRACT(month FROM TO_DATE(SPLIT_PART(i.periodo, \' - \', 1), \'DD/MM/YYYY\')) = EXTRACT(month FROM v.data)
  AND i.logistica = \'Entrega parceira\'
  WHERE EXTRACT(year FROM v.data) = 2026
  GROUP BY mes_num ORDER BY mes_num
'''

lines.insert(1741, novas_regras)
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
