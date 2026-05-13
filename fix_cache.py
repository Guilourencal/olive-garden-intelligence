lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if '@st.cache_data(ttl=3600)' in line and i < 160:
        lines[i] = '@st.cache_data(ttl=1)'
        print(f'Linha {i+1} alterada para ttl=1')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
