lines = open('atualizar_tudo.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if '("Classificando social...", "classificar_social.py"),' in line:
        lines.insert(i, '    ("Coletando Instagram...", "coletar_instagram.py"),')
        break
open('atualizar_tudo.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('Feito!')
