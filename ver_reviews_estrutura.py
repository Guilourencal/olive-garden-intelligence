lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[286:600], 287):
    if 'section-title' in line or 'container' in line or 'st.metric' in line or '# ' in line:
        print(f'{i}: {line}', end='')
