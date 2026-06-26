content = open('test_fila_insert.py', 'r', encoding='utf-8').read()
print('status no vals:', 'status' in content)
# Mostrar a linha vals
for i, line in enumerate(content.split('\n')):
    if 'vals' in line:
        print(f'{i+1}: {line}')
