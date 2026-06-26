readme = open('README_ROTINAS.md', 'r', encoding='utf-8').read()
nova_rotina = '''
### Atualizar Reclamacoes Buzzmonitor (semanal):
`powershell
# 1. Salvar arquivo xlsx em:
#    C:\\olive-garden-reviews\\data\\reclamacoes\\
python importar_reclamacoes.py
`
'''
with open('README_ROTINAS.md', 'a', encoding='utf-8') as f:
    f.write(nova_rotina)
print('OK')
