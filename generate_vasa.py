#!python3
import os
from import_lib import *

out_dir = "output/"
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

################################
# CREATE IMG
################################
img_size = (500,1000)

# Create img
bg_img       = create_image(img_size,(0,39,48,255))
overlay_img  = create_image(img_size,(255,255,255,0))
overlay_img2 = create_image(img_size,(255,255,255,0))

# Create symbol
symbol_size   = (50,50)
symbol_color1 = (0,255,115)
symbol_color2 = (0,0,0)
symbol_colors = ( symbol_color1, symbol_color2 )
symbol_img   = create_symbol(symbol_size,symbol_colors,'rectangle')
symbol_img.save(out_dir+'symbol.png')

# Fill img with symbol
fill_image_with_symbol(overlay_img,symbol_img)

# Apply background to overlay
overlay_img = Image.alpha_composite( create_image(img_size,(0,0,0,255)), overlay_img)
overlay_img.save(out_dir+'overlay.png')

# Apply Gaussian filter
nb_symbol = ( int(img_size[0]/symbol_size[0]) , int(img_size[1]/symbol_size[1]) )
mu  = img_size[0]/2 - symbol_size[0]/2
sig = img_size[0]/5
gaussian_2d_fct(overlay_img,symbol_size,mu,sig,max_alpha=220,inv_fct=True)
overlay_img.save(out_dir+'overlay_gaussian_alpha.png')

# Merge background and overlay
bg_img = Image.alpha_composite(bg_img,overlay_img)
bg_img.save(out_dir+'vasa.png')

# Create symbol
symbol_colors = ( (0,20,24), (0,0,0) )
span = 0.05
symbol_img          = create_image(symbol_size,(0,0,0,0))
symbol_overlay_size = (int(symbol_size[0]*(1-span)),int(symbol_size[1]*(1-span)))
symbol_overlay = create_symbol(symbol_overlay_size,symbol_colors,'ellipse')
symbol_img.paste(symbol_overlay,(int(symbol_size[0]*(span/2.0)),int(symbol_size[1]*(span/2.0))))
symbol_img.save(out_dir+'symbol2.png')

# Fill img with symbol
fill_image_with_symbol(overlay_img2,symbol_img)

# Apply background to overlay
#overlay_img2 = Image.alpha_composite( create_image(img_size,(0,0,0,255)), overlay_img2)
overlay_img2.save(out_dir+'overlay2.png')

# Apply Gaussian filter
nb_symbol = ( int(img_size[0]/symbol_size[0]) , int(img_size[1]/symbol_size[1]) )
mu  = img_size[0]/2 - symbol_size[0]/2
sig = img_size[0]/5
gaussian_2d_fct(overlay_img2,symbol_size,mu,sig,max_alpha=255,inv_fct=False)
overlay_img2.save(out_dir+'overlay_gaussian_alpha2.png')

# Merge background and overlay
bg_img = Image.alpha_composite(bg_img,overlay_img2)
bg_img.save(out_dir+'vasa1.png')

#########################
# Sphere calc
#########################
new_img = bg_img
#new_img = sphere_engine(new_img, (0,             0             ,0), img_size[0]/2 * 2**0.5, 1.5)
new_img = sphere_engine(new_img, (img_size[0]/2, 0             ,0), img_size[0]/2, 1)
#new_img = sphere_engine(new_img, (img_size[0]-1, img_size[1]-1 ,0), img_size[0]/2 * 2**0.5, 1.5)
#new_img = sphere_engine(new_img, (0,             img_size[1]/2 ,0), img_size[0]/2, 1)
#new_img = sphere_engine(new_img, (img_size[0]/2, img_size[1]/2 ,0), img_size[0]/2, 1)

new_img.save(out_dir+'vasa2.png')

