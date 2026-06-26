content = open('dashboard.py', 'r', encoding='utf-8').read()

start = content.find('\nelif aba_sel == "Menu":')
end = content.find('\nst.markdown(\n    \'<div style="text-align:center; font-size:10px; color:#B8A898;')

print(f'Bloco Menu: linhas {content[:start].count(chr(10))+1} a {content[:end].count(chr(10))+1}')
print(f'Tamanho: {end-start} chars')
