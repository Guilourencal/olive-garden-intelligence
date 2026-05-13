import pandas as pd
import glob
import os

arquivos = glob.glob("data/ifood_vendas/*.xlsx")
for a in arquivos:
    print(os.path.basename(a))
