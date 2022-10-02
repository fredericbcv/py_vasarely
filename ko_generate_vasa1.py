#!python3
from import_lib import *

out_dir = "output/"
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

################################
# CREATE IMG
################################
img_size = (500,500)

# Create img
bg_img      = create_image(img_size,(0,39,48,255))
overlay_img = create_image(img_size,(255,255,255,0))

# Create symbol
symbol_size   = (20,20)
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
sig = (img_size[0]/2*1.5)/4
gaussian_2d_fct(overlay_img,(50,50),mu,sig)
overlay_img.save(out_dir+'overlay_gaussian_alpha.png')

# Merge background and overlay
bg_img = Image.alpha_composite(bg_img,overlay_img)
bg_img.save(out_dir+'vasa.png')

# create_all_symbol(  overlay_img,\
#                     'rectangle',\
#                     nb_symbol,\
#                     symbol_size,\
#                     symbol_color,\
#                     0.0,\
#                     mu,\
#                     sig, \
#                     None, \
#                     160, \
#                     alpha_fct=False, \
#                     color_fct=True, \
#                     inv_color=True \
#                     )
# bg_img = Image.alpha_composite(bg_img,overlay_img)

# # Create ellipse
# overlay_img = create_image(img_size,(255,255,255,0))
# #symbol_color = (0,20,50)
# symbol_color = (0,39,48)
# create_all_symbol(  overlay_img,\
#                     'ellipse',\
#                     nb_symbol,\
#                     symbol_size,\
#                     symbol_color,\
#                     0.05,\
#                     mu,\
#                     sig,\
#                     None, \
#                     160, \
#                     alpha_fct=True, \
#                     inv_alpha=False, \
#                     color_fct=True, \
#                     inv_color=True \
#                     )
# bg_img = Image.alpha_composite(bg_img,overlay_img)

# # Save image
# bg_img.save('vasa1.png')
