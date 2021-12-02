#!python3
from PIL import Image, ImageDraw
from matplotlib import pyplot as mp
import numpy as np
import math

############################################################
# Functions
############################################################
def create_image(img_size,img_color):
    return Image.new('RGBA', img_size, img_color)


def gaussian_fct(x,mu,sig):
    return np.exp(-np.power(x - mu, 2.)/(2 * np.power(sig,2)))
    
    #x_values = np.linspace(0,nb_symbol[0],120)
    #mp.plot(x_values, gaussian_fct(x_values,mu,sig))
    #mp.show()


def create_symbol(draw,shape,position,symbol_format,span):
    span_symbol = int(symbol_format[0]*span)
    x           = position[0] * symbol_format[0] + span_symbol/2
    y           = position[1] * symbol_format[0] + span_symbol/2
    size        = symbol_format[0] - span_symbol
    ft_color    = symbol_format[1]
    if shape == 'ellipse':
        draw.ellipse( (x,y,x+size,y+size), fill=ft_color )
    else:
        draw.rectangle( (x,y,x+size,y+size), fill=ft_color )


def gaussian_square(x,y,nb_symbol,inv_fct,mu,sig):
    if y < (nb_symbol[1]/2):
        if x >= y and x < nb_symbol[0]-y:
            if inv_fct:
                return gaussian_fct(nb_symbol[0]/2-y,mu,sig)
            else:
                return gaussian_fct(y,mu,sig)
        else:
            if inv_fct:
                return gaussian_fct(abs(nb_symbol[0]/2-x),mu,sig)
            else:
                return gaussian_fct(x,mu,sig)
    else:
        if x >= nb_symbol[1]-y and x < nb_symbol[0]-(nb_symbol[1]-1-y):
            if inv_fct:
                return gaussian_fct(abs(nb_symbol[0]/2-(nb_symbol[1]-1-y)),mu,sig)
            else:
                return gaussian_fct(nb_symbol[1]-1-y,mu,sig)

        else:
            if inv_fct:
                return gaussian_fct(abs(nb_symbol[0]/2-x),mu,sig)
            else:
                return gaussian_fct(x,mu,sig)


def create_all_symbol(img,shape,nb_symbol,symbol_size,symbol_color,span,mu,sig,max_alpha=255,alpha_fct=True,inv_alpha=False,color_fct=True,inv_color=False):
    draw = ImageDraw.Draw(img)
    #max_alpha = 230     # 192

    for y in range(nb_symbol[1]):
        for x in range(nb_symbol[0]):

            # Set alpha
            if alpha_fct:
                alpha = gaussian_square(x,y,nb_symbol,inv_alpha,mu,sig)*max_alpha
                alpha = int(alpha)
            else:
                alpha = max_alpha

            # Set color_factor
            if color_fct:
                color_factor = gaussian_square(x,y,nb_symbol,inv_color,mu,sig)
            else:
                color_factor = 1.0

            # Apply color_factor
            tmp_symbol_color =  (   symbol_color[0]*color_factor, \
                                    symbol_color[1]*color_factor, \
                                    symbol_color[2]*color_factor, \
                                    alpha \
                                )

            # Cast values
            tmp_symbol_color =  (   int(tmp_symbol_color[0]), \
                                    int(tmp_symbol_color[1]), \
                                    int(tmp_symbol_color[2]), \
                                    alpha \
                                )

            # Set symbol format
            symbol_format = ( symbol_size, tmp_symbol_color )

            # Adding symbol
            create_symbol(draw,shape,(x,y),symbol_format,span)

def spherize_coordinates(p , c, radius, curvature):
    # https://lms.fun-mooc.fr/asset-v1:ulb+44013+session03+type@asset+block/explication-deformation.pdf

    # Coordinates
    x, y, z = p
    x_,y_,z_= p
    xc, yc, zc = int(c[0]), int(c[1]), int(c[2])

    # relative coordinates
    x_minus_xc = x - xc
    y_minus_yc = y - yc
    z_minus_zc = z - zc

    # Apparent radius
    #Ra = math.sqrt( radius**2 - z_minus_zc**2 )

    # Norm radius
    r = math.sqrt( x_minus_xc**2 + y_minus_yc**2 )

    if 0 < r < radius:
        #r_div_Ra = r / Ra
        r_div_Ra = r / radius
        #r_ = radius * math.sin( r_div_Ra * math.acos( abs(z_minus_zc) / radius ) )
        r_ = radius * math.sin( r_div_Ra * (math.pi/2) )

        # New coordinates
        x_ = xc + (r / r_)**curvature * x_minus_xc
        y_ = yc + (r / r_)**curvature * y_minus_yc

    return x_,y_,z_

def tuple_add(t1,t2):
    if len(t1) == len(t2):
        ret_tuple = tuple()
        for i in range(len(t1)):
            ret_tuple += (t1[i]+t2[i],)
    return ret_tuple

def tuple_sub(t1,t2):
    if len(t1) == len(t2):
        ret_tuple = tuple()
        for i in range(len(t1)):
            ret_tuple += (t1[i]-t2[i],)
    return ret_tuple

def tuple_int(t):
    ret_tuple = tuple()
    for i in range(len(t)):
        ret_tuple += (int(t[i]),)
    return ret_tuple

def linear_interpolation(x,y, x_,y_, img_size, original_pixels, new_pixels):
    # https://fr.wikipedia.org/wiki/Interpolation_lin%C3%A9aire
    # f(x) = y1 * (x2-x)/(x2-x1) + y2 * (x-x1)/(x2-x1)
    #
    # x1 = 0 & x2 = 1
    #
    # f(x) = y1 * (1-x_frac) + y2 * x_frac

    # Get int & frac value
    x_int   = int(x_)
    x_frac  = x_ - x_int
    y_int   = int(y_)
    y_frac  = y_ - y_int

    # Edge management
    if x_int < img_size[0]-1:
        x_int_add_1 = x_int+1
    else:
        x_int = img_size[0]-1
        x_int_add_1 = img_size[0]-1
    if y_int < img_size[1]-1:
        y_int_add_1 = y_int+1
    else:
        y_int = img_size[1]-1
        y_int_add_1 = y_int

    if x_frac == 0:
        # y interpolation
        y1 = original_pixels[x_int, y_int] 
        y2 = original_pixels[x_int, y_int_add_1] 
        y1 = tuple(map(lambda value: value * (1-y_frac), y1))
        y2 = tuple(map(lambda value: value * y_frac,     y2))

    else:
        # x interpolation
        y1 = original_pixels[x_int,  y_int] 
        y2 = original_pixels[x_int_add_1,y_int] 
        y1 = tuple(map(lambda value: value * (1-x_frac), y1))
        y2 = tuple(map(lambda value: value * x_frac,     y2))

    new_pixels[x,y] = tuple_int(tuple_add(y1,y2))


def bilinear_interpolation(x,y, x_,y_, img_size, original_pixels, new_pixels):
    # https://fr.wikipedia.org/wiki/Interpolation_bilin%C3%A9aire
    #
    #   (x1,y2)         (x2,y2)
    #
    #            (x,y)  
    #
    #   (x1,y1)         (x2,y1)
    #
    # f(x,y) =  ( f(x2,y1) - f(x1,y1) ) * (x-x1)/(x2-x1) + 
    #           ( f(x1,y2) - f(x1,y1) ) * (y-y1)/(y2-y1) + 
    #           ( f(x1,y1) + f(x2,y2) - f(x2,y1) - f(x1,y2) ) * (x-x1) / (x2-x1) * (y-y1)/(y2-y1) +
    #           f(x1,y1)
    #
    # x1 = y1 = 0 & x2 = y2 = 1
    #
    # f(x,y) =  ( f(x2,y1) - f(x1,y1) ) * x_frac + 
    #           ( f(x1,y2) - f(x1,y1) ) * y_frac + 
    #           ( f(x1,y1) + f(x2,y2) - f(x2,y1) - f(x1,y2) ) * x_frac * y_frac +
    #           f(x1,y1)

    # Get int & frac value
    x_int   = int(x_)
    x_frac  = x_ - x_int
    y_int   = int(y_)
    y_frac  = y_ - y_int

    # Edge management
    if x_int < img_size[0]-1:
        x_int_add_1 = x_int+1
    else:
        x_int = img_size[0]-1
        x_int_add_1 = img_size[0]-1
    if y_int < img_size[1]-1:
        y_int_add_1 = y_int+1
    else:
        y_int = img_size[1]-1
        y_int_add_1 = y_int

    # No treatement
    if x_frac == 0 and y_frac == 0:
        return None

    # linear_interpolation
    if x_frac == 0 or y_frac == 0:
        linear_interpolation(x,y,x_,y_,img_size,original_pixels, new_pixels)

    else:
        f11 = original_pixels[x_int,y_int]
        f12 = original_pixels[x_int,y_int_add_1]
        f21 = original_pixels[x_int_add_1,y_int]
        f22 = original_pixels[x_int_add_1,y_int_add_1]

        tmp1 = tuple(map(lambda value: value * x_frac, tuple_sub(f21,f11)))
        tmp2 = tuple(map(lambda value: value * y_frac, tuple_sub(f12,f11)))
        tmp3 = tuple(map(lambda value: value * x_frac * y_frac, tuple_sub(tuple_sub(tuple_add(f11,f22),f21),f12)))

        tmp4 = tuple_add( tuple_add( tuple_add(tmp1,tmp2), tmp3), f11)

        new_pixels[x,y] = tuple_int(tmp4)
