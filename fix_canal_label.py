lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

# Adicionar label de plataforma apos canal_icon na linha 471 (antes do for)
lines[470] = '            canal_icon = "📱 Instagram" if row["canal"] == "instagram" else "🔍 Google"\n'

open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
