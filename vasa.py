#!python3
from vasa_lib import *

nb_symbol     = (20,20)
symbol_size   = 500
img_size      = (symbol_size*nb_symbol[0],symbol_size*nb_symbol[1])

# Set Gaussian values
mu  = (nb_symbol[0]-1)/2
sig = nb_symbol[0]/5

# Create background img
bg_img      = create_image(img_size,(0,39,48,255))

# Create rectangle
overlay_img = create_image(img_size,(255,255,255,0))
symbol_color = (0,255,115)
create_all_symbol(  overlay_img,\
                    'rectangle',\
                    nb_symbol,\
                    symbol_size,\
                    symbol_color,\
                    0.0,\
                    mu,\
                    sig, \
                    160, \
                    alpha_fct=False, \
                    color_fct=True, \
                    inv_color=True \
                    )
bg_img = Image.alpha_composite(bg_img,overlay_img)

# Create ellipse
overlay_img = create_image(img_size,(255,255,255,0))
#symbol_color = (0,20,50)
symbol_color = (0,39,48)
create_all_symbol(  overlay_img,\
                    'ellipse',\
                    nb_symbol,\
                    symbol_size,\
                    symbol_color,\
                    0.05,\
                    mu,\
                    sig,\
                    160, \
                    alpha_fct=True, \
                    inv_alpha=False, \
                    color_fct=True, \
                    inv_color=True \
                    )
bg_img = Image.alpha_composite(bg_img,overlay_img)

# Save image
bg_img.save('vasa.png')
