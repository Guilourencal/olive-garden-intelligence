import os
from datetime import datetime
pasta = r'C:\olive-garden-reviews\data\ifood_vendas'
for f in sorted(os.listdir(pasta)):
    caminho = os.path.join(pasta, f)
    mt = os.path.getmtime(caminho)
    print(datetime.fromtimestamp(mt).strftime('%d/%m/%Y %H:%M') + ' — ' + f)
