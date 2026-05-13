import base64

with open('assets/Olivia_Fundo_Branco_Header.png', 'rb') as f:
    data = base64.b64encode(f.read()).decode('utf-8')

print(f'Tamanho base64: {len(data)} caracteres')
print(f'Primeiros 50: {data[:50]}')
