#!python3
from numpy import *
from vasa_lib import *
from interpolate import *
import inspect 

#########################
# FUNCTIONS
#########################
def sphere_engine(img_obj,img_size, pc, radius, curvature=1):
    # 1 < curvature < N

    # Copy input img
    new_img  = img_obj.copy()
    new_img.load()[0,0] = (0,0,0,255)

    # Create array
    img_array       = list(range(img_size[0]))
    img_matrix      = []
    original_pixels = img_obj.load()
    new_pixels      = new_img.load()

    spherized_coordinates = list()

    for y in range(img_size[1]):
        for x in range(img_size[0]):
            # Calculate new points
            x_,y_,z_ = spherize_coordinates((x,y,0),pc,radius,curvature)
            spherized_coordinates.append([x,y,x_,y_])

            # New pixel to calculate ? 
            if type(x_) == int and type(y_) == int:
                continue

            # Interpolation bilineaire
            if type(x_) != int and type(y_) != int:
                bilinear_interpolation(x,y,x_,y_,img_size,original_pixels,new_pixels)

            # Interpolation linaire
            else:
                linear_interpolation(x,y,x_,y_,img_size,original_pixels,new_pixels)

    return new_img


#########################
# CREATE IMG
#########################
img_size = (500,500)

# Create background img
bg_img      = create_image(img_size,(154,185,183,255))

# Create rectangle
overlay_img = create_image(img_size,(255,255,255,0))
symbol_color = (242,198,27)
symbol_color2 = (5,26,104)

symbol_size = 50
nb_symbol = ( int(img_size[0]/symbol_size) , int(img_size[1]/symbol_size) )

mu  = (nb_symbol[0]-1)/2
sig = nb_symbol[0]/5

create_all_symbol(  overlay_img,\
                    'cube',\
                    nb_symbol,\
                    symbol_size,\
                    symbol_color,\
                    0.0,\
                    mu,\
                    sig, \
                    symbol_color2,\
                    160, \
                    alpha_fct=False, \
                    color_fct=False, \
                    inv_color=True \
                    )
bg_img = Image.alpha_composite(bg_img,overlay_img)
bg_img.save('sphere.png')

#########################
# Sphere calc
#########################
new_img = bg_img
#new_img = sphere_engine(new_img, img_size, (0,             0             ,0), img_size[0]/2 * 2**0.5, 1.5)
#new_img = sphere_engine(new_img, img_size, (img_size[0]-1, 0             ,0), img_size[0]/2, 1.5)
#new_img = sphere_engine(new_img, img_size, (img_size[0]-1, img_size[1]-1 ,0), img_size[0]/2 * 2**0.5, 1.5)
#new_img = sphere_engine(new_img, img_size, (0,             img_size[1]-1 ,0), img_size[0]/2, 1.5)
new_img = sphere_engine(new_img, img_size, (img_size[0]/2, img_size[1]/2 ,0), img_size[0]/2, 1)

new_img.save('sphere1_bilinear_interpol.png')

