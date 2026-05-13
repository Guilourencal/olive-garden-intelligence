lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
lines[657] = '                st.markdown('
del lines[658]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('Feito!')
