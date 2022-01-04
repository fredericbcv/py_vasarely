#!python3
import inspect
from numpy import *
from import_lib import *

out_dir = "output/"
if not os.path.isdir(out_dir):
	os.makedirs(out_dir)

################################
# CREATE IMG
################################
img_size = (500,500)

# Create img
#bg_img      = create_image(img_size,(154,185,183,255))
bg_img      = create_image(img_size,(242,198,27,255))
overlay_img = create_image(img_size,(255,255,255,0))

# Create symbol
symbol_size = (50,100)
symbol_color1 = (242,198,27)
symbol_color2 = (5,26,104)
symbol_colors = ( symbol_color1, symbol_color2 )
#symbol_img    = create_image(symbol_size,(0,0,0,0))
#ellipse_img   = create_symbol((22,22),symbol_colors,'cube')
#symbol_img.paste(ellipse_img,(1,1))
symbol_img   = create_symbol(symbol_size,symbol_colors,'cube')
symbol_img.save(out_dir+'symbol.png')

# Fill img with symbol
fill_image_with_symbol(overlay_img,symbol_img)

# Apply background to overlay
overlay_img = Image.alpha_composite( create_image(img_size,(0,0,0,255)), overlay_img)
overlay_img.save(out_dir+'overlay.png')

# Apply Gaussian filter
nb_symbol = ( int(img_size[0]/symbol_size[0]) , int(img_size[1]/symbol_size[1]) )
mu  = img_size[0]/2
sig = img_size[0]/2*1.5
gaussian_2d_fct(overlay_img,(25,25),mu,sig)
overlay_img.save(out_dir+'overlay_gaussian_alpha.png')

# Merge background and overlay
bg_img = Image.alpha_composite(bg_img,overlay_img)
bg_img.save(out_dir+'sphere.png')

################################
# Sphere calc
################################
new_img = bg_img
#new_img = sphere_engine(new_img, (img_size[0]/2, 0 ,0), img_size[0]/2, 1)
#new_img = sphere_engine(new_img, (img_size[0]/2, img_size[1] ,0), img_size[0]/2, 1)
new_img = sphere_engine(new_img, (img_size[0]/2, img_size[1]/2 ,0), img_size[0]/2, 1)
new_img.save(out_dir+'sphere1.png')

