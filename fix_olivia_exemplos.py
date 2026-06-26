lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

exemplos_corretos = '''
VALORES REAIS DO BANCO (use como referencia para validar suas queries):
- Venda Salao YTD 2026 Morumbi: ~R$ 13.3M | Aricanduva: ~R$ 4.1M
- iFood YTD 2026 (Entrega parceira apenas): Morumbi R$ 446k | Aricanduva R$ 232k | Center Norte R$ 348k | Dom Pedro R$ 173k
- NUNCA some venda_salao como faturamento iFood — sao tabelas diferentes
- Para faturamento iFood use SEMPRE: SELECT SUM(faturamento) FROM ifood_vendas WHERE logistica = 'Entrega parceira'
- Para share iFood: faturamento_ifood / (venda_salao + faturamento_ifood) * 100
- ifood_vendas tem apenas 4 filiais: Morumbi, Center Norte, Dom Pedro, Aricanduva
- GRU2 e GRU3 NAO tem iFood — nunca inclua no calculo de share iFood
- Queries de share devem filtrar vendas_diarias apenas para as 4 filiais com iFood quando comparando com iFood

QUERY CORRETA para share iFood por filial YTD 2026:
SELECT
    i.filial,
    SUM(i.faturamento) as fat_ifood,
    SUM(v.venda_salao) as fat_salao,
    ROUND(SUM(i.faturamento)::numeric / NULLIF((SUM(i.faturamento) + SUM(v.venda_salao))::numeric, 0) * 100, 1) as share_ifood
FROM ifood_vendas i
JOIN vendas_diarias v ON v.filial = i.filial
    AND EXTRACT(month FROM TO_DATE(SPLIT_PART(i.periodo, \' - \', 1), \'DD/MM/YYYY\')) = EXTRACT(month FROM v.data)
    AND EXTRACT(year FROM v.data) = 2026
WHERE i.logistica = \'Entrega parceira\'
GROUP BY i.filial
ORDER BY share_ifood DESC

'''

# Inserir antes do fechamento """
lines.insert(1738, exemplos_corretos)
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
