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
    new_img2 = img_obj.copy()
    new_img2.load()[0,0] = (0,0,0,255)

    # Create array
    img_array       = list(range(img_size[0]))
    img_matrix      = []
    original_pixels = img_obj.load()
    new_pixels      = new_img.load()
    new_pixels2     = new_img2.load()

    spherized_coordinates = list()

    for y in range(img_size[1]):
        for x in range(img_size[0]):
            # Calculate new points
            x_,y_,z_ = spherize_coordinates((x,y,0),pc,radius,curvature)
            spherized_coordinates.append([x,y,x_,y_])

    # X interpolation
    for coordinate in spherized_coordinates:
        x,y,x_,y_ = coordinate

        # Ignore true pixel
        if type(x_) == int:
            continue

        # Get coeffs
        x_frac = x_ - int(x_)
        coeff = convolution_coeff(x_frac)

        # Get pixel position
        x_2 = int(x_)-2
        x_1 = int(x_)-1
        x0  = int(x_)
        x1  = int(x_)+1
        x2  = int(x_)+2
        x3  = int(x_)+3

        # Edge management
        if x_2 < 0:
            x_2 = 0
        if x_1 < 0:
            x_1 = 0
        if x1 > img_size[0]-1:
            x1 = img_size[0]-1
        if x2 > img_size[0]-1:
            x2 = img_size[0]-1
        if x3 > img_size[0]-1:
            x3 = img_size[0]-1

        # Get pixel
        x_2 = original_pixels[x_2,int(y)]
        x_1 = original_pixels[x_1,int(y)]
        x0  = original_pixels[x0,int(y)]
        x1  = original_pixels[x1,int(y)]
        x2  = original_pixels[x2,int(y)]
        x3  = original_pixels[x3,int(y)]

        # Mult by coeff
        x_2 = tuple_int(tuple(map(lambda value: value * coeff[0], x_2)))
        x_1 = tuple_int(tuple(map(lambda value: value * coeff[1], x_1)))
        x0  = tuple_int(tuple(map(lambda value: value * coeff[2], x0)))
        x1  = tuple_int(tuple(map(lambda value: value * coeff[3], x1)))
        x2  = tuple_int(tuple(map(lambda value: value * coeff[4], x2)))
        x3  = tuple_int(tuple(map(lambda value: value * coeff[5], x3)))

        # Sum all
        tmp_pixel1 = tuple_add(x_2,x_1)
        tmp_pixel2 = tuple_add(x0,x1)
        tmp_pixel3 = tuple_add(x2,x3)
        tmp_pixel4 = tuple_add(tmp_pixel1,tmp_pixel2)
        tmp_pixel5 = tuple_add(tmp_pixel3,tmp_pixel4)
        new_pixels[x,y] = tuple_int(tmp_pixel5)
        new_pixels[x,y] = (new_pixels[x,y][0],new_pixels[x,y][1],new_pixels[x,y][2],original_pixels[x,y][3])

    # # Y interpolation
    for coordinate in spherized_coordinates:
        x,y,x_,y_ = coordinate

        # Ignore true pixel
        if type(y_) == int:
            continue

        # Get coeffs
        y_frac = y_ - int(y_)
        coeff = convolution_coeff(y_frac)

        # Get pixel position
        y_2 = int(y_)-2
        y_1 = int(y_)-1
        y0  = int(y_)
        y1  = int(y_)+1
        y2  = int(y_)+2
        y3  = int(y_)+3

        # Edge management
        if y_2 < 0:
            y_2 = 0
        if y_1 < 0:
            y_1 = 0
        if y1 > img_size[1]-1:
            y1 = img_size[1]-1
        if y2 > img_size[1]-1:
            y2 = img_size[1]-1
        if y3 > img_size[1]-1:
            y3 = img_size[1]-1

        # Get pixel
        y_2 = new_pixels[int(x),y_2]
        y_1 = new_pixels[int(x),y_1]
        y0  = new_pixels[int(x),y0]
        y1  = new_pixels[int(x),y1]
        y2  = new_pixels[int(x),y2]
        y3  = new_pixels[int(x),y3]

        # Mult by coeff
        y_2 = tuple(map(lambda value: value * coeff[0], y_2))
        y_1 = tuple(map(lambda value: value * coeff[1], y_1))
        y0  = tuple(map(lambda value: value * coeff[2], y0))
        y1  = tuple(map(lambda value: value * coeff[3], y1))
        y2  = tuple(map(lambda value: value * coeff[4], y2))
        y3  = tuple(map(lambda value: value * coeff[5], y3))

        # Sum all
        tmp_pixel1 = tuple_add(y_2,y_1)
        tmp_pixel2 = tuple_add(y0,y1)
        tmp_pixel3 = tuple_add(y2,y3)
        tmp_pixel4 = tuple_add(tmp_pixel1,tmp_pixel2)
        tmp_pixel5 = tuple_add(tmp_pixel3,tmp_pixel4)
        new_pixels2[x,y] = tuple_int(tmp_pixel5)
        new_pixels2[x,y] = (new_pixels2[x,y][0],new_pixels2[x,y][1],new_pixels2[x,y][2],original_pixels[x,y][3])

    return new_img2


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

new_img.save('sphere1.png')

