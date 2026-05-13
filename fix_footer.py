with open('dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

footer = '''st.markdown(
    '<div style="text-align:center; font-size:10px; color:#B8A898; letter-spacing:0.1em; padding-top:20px;">'
    'OLIVE GARDEN BRAND INTELLIGENCE © 2026</div>',
    unsafe_allow_html=True
)'''

olivia_start = '\nelif aba_sel == "OlivIA":'

content = content.replace(footer + '\n' + olivia_start, olivia_start)
content = content.rstrip() + '\n\n' + footer + '\n'

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')
