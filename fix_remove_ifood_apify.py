lines = open('atualizar_tudo.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if '("Coletando iFood...", "coletar_ifood.py"),' in line:
        lines[i] = '    # iFood agora via relatorio oficial — ver importar_ifood_reviews.py'
        print(f'Linha {i+1} removida!')
        break
open('atualizar_tudo.py', 'w', encoding='utf-8').write('\n'.join(lines))
