#!python3
import os, functools
import numpy as np

################################
# TUPLE OPERATIONS
################################
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

def tuple_round(t):
    ret_tuple = tuple()
    for i in range(len(t)):
        ret_tuple += (round(t[i]),)
    return ret_tuple

def tuple_cast(t,min_val=0,max_val=255):
    ret_tuple = tuple()
    for i in range(len(t)):
        if t[i] < min_val:
            ret_tuple += (min_val,)
        elif t[i] > max_val:
            ret_tuple += (max_val,)
        else:
            ret_tuple += (t[i],)
    return ret_tuple


################################
# CONVOLUTION FUNCTION
################################
# https://clouard.users.greyc.fr/Pantheon/experiments/rescaling/index-fr.html
def nearest_neighbor_fct(x):
    if x >= 0.5:
        return 0;
    elif -0.5 <= x < 0.5:
        return 1
    else:
        return 0

def linear_fct(x):
    if abs(x) < 1:
        return 1-abs(x)
    else:
        return 0

def bicubic_fct(x,a=-0.5):
    if abs(x) <= 1:
        return (a+2)*abs(x)**3 - (a+3)*abs(x)**2+1 
    elif 1 < abs(x) < 2:
        return a*abs(x)**3 - 5*a*abs(x)**2 + 8*a*abs(x) - 4*a
    else:
        return 0

def mitchell_netravali_fct(x,b=1/3,c=1/3):
    if abs(x) < 1:
        return (1/6)*( (12-9*b-6*c)*abs(x)**3 + (-18+12*b+6*c)*abs(x)**2 + (6-2*b) )
    elif 1 <= abs(x) < 2:
        return (1/6)*( (-b-6*c)*abs(x)**3 + (6*b+30*c)*abs(x)**2 + (-12*b-48*c)*abs(x) + (8*b+24*c) )
    else:
        return 0

def smoothed_quadratic_fct(x):
    # https://zipcpu.com/dsp/2018/01/16/interpolation-is-convolution.html
    if -3/2 <= x < -1/2:
        return 1/2*x**2 + 3/2*x + 9/8
    elif -1/2 <= x < 1/2:
        return 3/4-x**2
    elif 1/2 <= x < 3/2:
        return 1/2*x**2 - 3/2*x + 9/8
    else:
        return 0

def lanczos_fct(x,a=3):
    if abs(x) < a:
        return np.sinc(x) * np.sinc(x/a)
    else:
        return 0

def better_quadratic_fct(x,a2=-2/16,b2=-1/16,c2=0,a1=1,b1=10/16,c1=0,a0=-28/16):
    # https://zipcpu.com/dsp/2018/03/30/quadratic.html
    if -5/2 < x <= -3/2:
        return a2*(x+2)**2 + b2*(x+2) + c2
    elif -3/2 < x <= -1/2:
        return a1*(x+1)**2 + b1*(x+1) + c1
    elif -1/2 < x <= 1/2:
        return a0*x**2 + 1
    elif 1/2 < x <= 3/2:
        return a1*(-x+1)**2 + b1*(-x+1) + c1
    elif 3/2 < x <= 5/2:
        return a2*(-x+2)**2 + b2*(-x+2) + c2
    else:
        return 0

def convolution_get_coeffs(x,filter_size=6,fct_name=bicubic_fct):
    # https://fr.wikipedia.org/wiki/Produit_de_convolution
    # f*g(x) = E f(x-m)g(m) = E f(m)g(x-m)
    filter_center = int((filter_size-1)/2)
    coeffs = list()

    # Check fct validity
    fct_validity = False
    if fct_name in [nearest_neighbor_fct,linear_fct] and filter_size >= 2:
        fct_validity = True
    if fct_name in [bicubic_fct,mitchell_netravali_fct,smoothed_quadratic_fct] and filter_size >= 4:
        fct_validity = True
    if fct_name in [lanczos_fct,better_quadratic_fct] and filter_size >= 6:
        fct_validity = True
    if not fct_validity:
        raise ValueError ("fct_convolution and filter_size does not match")

    # Calc coeff
    # Example with filter_size = 6 
    # coeffs[5] = fct_name(x-3) #  3-x
    # coeffs[4] = fct_name(x-2) #  2-x
    # coeffs[3] = fct_name(x-1) #  1-x
    # coeffs[2] = fct_name(x-0) #   -x
    # coeffs[1] = fct_name(x+1) # -1-x
    # coeffs[0] = fct_name(x+2) # -2-x
    for i in range(filter_size):
        coeffs.append( fct_name( x - (i-filter_center) ) )

    return coeffs

def convolution_get_pixels(x,y,img_obj,filter_size=6,axis="x"):
    pixels_value = list()
    pixels_index = list()
    filter_center = int((filter_size-1)/2)

    # Get pixel position
    for i in range(filter_size):
        if axis == "x":
            pixels_index.append( x - filter_center + i )
        else:
            pixels_index.append( y - filter_center + i )

    # Edge management
    for i, index in enumerate(pixels_index):
        if index < 0:
            index = 0
        if axis == "x":
            if index > img_obj.size[0]-1:
                pixels_index[i] = img_obj.size[0]-1
        else:
            if index > img_obj.size[1]-1:
                pixels_index[i] = img_obj.size[1]-1

    # Get pixel
    for index in pixels_index:
        if axis == "x":
            pixels_value.append( img_obj.getpixel( (index,y) ) )
        else:
            pixels_value.append( img_obj.getpixel( (x,index) ) )

    return pixels_value

def convolution_1d_fct(coeffs,pixels):
    # Check input len equality
    if len(coeffs) != len(pixels):
        raise ValueError ("coeffs and pixels must have same size")

    # Mult each coeff by pixel_val
    tmp_val = list()
    for i in range(len(coeffs)):
        tmp_val.append( tuple(map(lambda value: value * coeffs[i], pixels[i])) )

    # Sum all
    tmp_val = functools.reduce(lambda a,b: tuple_add(a,b),tmp_val)

    return tuple_round(tmp_val)


################################
# INTERPOLATION FUNCTION
################################
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

    # No treatement
    if x_frac == 0 and y_frac == 0:
        return None

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

