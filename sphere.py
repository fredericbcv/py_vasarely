#!python3
from numpy import *
from vasa_lib import *
import inspect 

#########################
# FUNCTIONS
#########################
def sphere_engine(img_obj,img_size):

    # Copy input img
    new_img = img_obj.copy()
    new_img.load()[0,0] = (0,0,0,255)

    # Create array
    img_array       = list(range(img_size[0]))
    img_matrix      = []
    original_pixels = img_obj.load()
    new_pixels      = new_img.load()

    for y in range(img_size[1]):
        #img_matrix.append( list(map(lambda x: deformation( (x,y,0), (100,100,0) , 50 )[:2], img_array)) )

        for x in range(img_size[0]):
            # Calculate new points
            x_,y_,z_ = deformation( (x,y,0), (250,0,0) , 250 )

            # New pixel to calculate ? 
            #if type(x_) == int and type(y_) == int:
            #    continue

            # Interpolation bilineaire
            if type(x_) != int and type(y_) != int:
                bilinear_interpolation(x,y,x_,y_,original_pixels,new_pixels)

            # Interpolation linaire
            #else:
            #    linear_interpolation(x,y,x_,y_,original_pixels,new_pixels)

            # Calc new points
            x_,y_,z_ = deformation( (x,y,0), (250,499,0) , 250 )

            # Interpolation bilineaire
            if type(x_) != int and type(y_) != int:
                bilinear_interpolation(x,y,x_,y_,original_pixels,new_pixels)

    return new_img


#########################
# CREATE IMG
#########################
img_size = (500,500)

# Create background img
bg_img      = create_image(img_size,(0,39,48,255))

# Create rectangle
overlay_img = create_image(img_size,(255,255,255,0))
symbol_color = (0,255,115)

symbol_size = 20
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
                    160, \
                    alpha_fct=False, \
                    color_fct=True, \
                    inv_color=True \
                    )
bg_img = Image.alpha_composite(bg_img,overlay_img)
bg_img.save('sphere.png')

#########################
# Sphere calc
#########################
new_img = sphere_engine(bg_img,img_size)
new_img.save('sphered.png')

