content = open('coletar_reclameaqui.py', 'r', encoding='utf-8').read()
content = content.replace('viralanalyzer/reclameaqui-scraper', 'epctex/reclame-aqui-scraper')
content = content.replace(
    '"companies": ["olive-garden"],\n        "maxComplaints": 100,\n        "statusFilter": "all",\n        "includeCompanyStats": True,',
    '"startUrls": [{"url": "https://www.reclameaqui.com.br/empresa/olive-garden/lista-reclamacoes/"}],\n        "maxItems": 100,'
)
open('coletar_reclameaqui.py', 'w', encoding='utf-8').write(content)
print('Feito!')
