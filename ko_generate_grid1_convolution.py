#!python3
import inspect
from vasa_lib import *

#########################
# CREATE IMG
#########################
img_size = (200,200)

# Create background img
bg_img      = create_image(img_size,(0,0,0,255))

# Create rectangle
overlay_img = create_image(img_size,(255,255,255,0))
symbol_color = (255,255,255)
symbol_color2 = (0,0,0)

symbol_size = 40
nb_symbol = ( int(img_size[0]/symbol_size) , int(img_size[1]/symbol_size) )

mu  = (nb_symbol[0]-1)/2
sig = nb_symbol[0]/5

create_all_symbol(  overlay_img,\
                    'rectangle',\
                    nb_symbol,\
                    symbol_size,\
                    symbol_color,\
                    0.2,\
                    mu,\
                    sig, \
                    symbol_color2,\
                    255, \
                    alpha_fct=False, \
                    color_fct=False, \
                    inv_color=True \
                    )
bg_img = Image.alpha_composite(bg_img,overlay_img)
bg_img.save('grid.png')

#########################
# Sphere calc
#########################
new_img = bg_img
#new_img = sphere_engine(new_img, (0,             0             ,0), img_size[0]/2 * 2**0.5, 1.5)
#new_img = sphere_engine(new_img, (img_size[0]-1, 0             ,0), img_size[0]/2, 1.5)
#new_img = sphere_engine(new_img, (img_size[0]-1, img_size[1]-1 ,0), img_size[0]/2 * 2**0.5, 1.5)
#new_img = sphere_engine(new_img, (0,             img_size[1]-1 ,0), img_size[0]/2, 1.5)
new_img = sphere_engine(new_img, (img_size[0]/2, img_size[1]/2 ,0), img_size[0]/2, 1)

new_img.save('grid1.png')

