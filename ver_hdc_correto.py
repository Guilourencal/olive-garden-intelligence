import pandas as pd

# Calculo correto
dados = {
    'Aricanduva':    (484457, 27, 17),
    'Center Norte':  (884150, 41, 17),
    'Dom Pedro':     (636490, 32, 17),
    'GRU2':          (422351, 29, 17),
    'GRU3':          (341958, 30, 17),
    'Morumbi':      (1318018, 69, 17),
}
print('=== VENDA/HDC CORRETO (Venda Total / HDC) ===')
for filial, (venda, hdc, dias) in dados.items():
    vhdc = venda / hdc
    print(f'{filial}: R$ {vhdc:,.0f}/HDC | Venda: R$ {venda:,.0f} | HDC: {hdc}'.replace(',','.'))
