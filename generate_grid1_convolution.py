#!python3
import inspect
from import_lib import *

out_dir = "output/"
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

#########################
# CREATE IMG
#########################
img_size = (500,500)

# Create background img
bg_img      = create_image(img_size,(0,0,0,255))
overlay_img = create_image(img_size,(255,255,255,0))

# Create symbol
symbol_size = (20,20)
symbol_color1 = (255,255,255)
symbol_color2 = (0,0,0)
symbol_colors = (symbol_color1,symbol_color2)

span = 0.2
symbol_img          = create_image(symbol_size,(0,0,0,0))
symbol_overlay_size = (int(symbol_size[0]*(1-span)),int(symbol_size[1]*(1-span)))
symbol_overlay = create_symbol(symbol_overlay_size,symbol_colors,'rectangle')
symbol_img.paste(symbol_overlay,(int(symbol_size[0]*(span/2.0)),int(symbol_size[1]*(span/2.0))))
symbol_img.save(out_dir+'symbol.png')

# Fill img with symbol
fill_image_with_symbol(overlay_img,symbol_img)

# Apply background to overlay
overlay_img = Image.alpha_composite( create_image(img_size,(0,0,0,255)), overlay_img)
overlay_img.save(out_dir+'overlay.png')

# Apply Gaussian filter
#nb_symbol = ( int(img_size[0]/symbol_size[0]) , int(img_size[1]/symbol_size[1]) )
#mu  = img_size[0]/2
#sig = img_size[0]/2*1.5
#gaussian_2d_fct(overlay_img,(25,25),mu,sig)
#overlay_img.save(out_dir+'overlay_gaussian_alpha.png')

# Merge background and overlay
bg_img = Image.alpha_composite(bg_img,overlay_img)
bg_img.save(out_dir+'grid.png')

#########################
# Sphere calc
#########################
new_img = bg_img
#new_img = sphere_engine(new_img, (0,             0             ,0), img_size[0]/2 * 2**0.5, 1.5)
#new_img = sphere_engine(new_img, (img_size[0]-1, 0             ,0), img_size[0]/2, 1.5)
#new_img = sphere_engine(new_img, (img_size[0]-1, img_size[1]-1 ,0), img_size[0]/2 * 2**0.5, 1.5)
#new_img = sphere_engine(new_img, (0,             img_size[1]-1 ,0), img_size[0]/2, 1.5)
new_img = sphere_engine(new_img, (img_size[0]/2, img_size[1]/2 ,0), img_size[0]/2, 1)

new_img.save(out_dir+'grid1.png')

