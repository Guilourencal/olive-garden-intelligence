from PIL import Image
import base64

img = Image.open('static/Header_Olivia_V2.png')
print(f'Tamanho original: {img.size}')
print(f'Modo: {img.mode}')

# Converter para RGBA
img = img.convert('RGBA')
data = img.getdata()

# Encontrar bounding box sem areas brancas
import numpy as np
arr = np.array(img)
# Encontrar linhas nao brancas (qualquer pixel com R,G,B < 240)
mask = ~((arr[:,:,0] > 240) & (arr[:,:,1] > 240) & (arr[:,:,2] > 240))
rows = np.any(mask, axis=1)
cols = np.any(mask, axis=0)
rmin, rmax = np.where(rows)[0][[0,-1]]
cmin, cmax = np.where(cols)[0][[0,-1]]
print(f'Crop: {rmin},{cmin} -> {rmax},{cmax}')

img_crop = img.crop((cmin, rmin, cmax+1, rmax+1))
img_crop.save('static/olivia_banner_final.png', 'PNG')
print(f'Salvo: {img_crop.size}')
