#!python3
import os, math
from numpy import *
from lib_interpolate import *

################################
# SPHERIZE
################################
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


def sphere_engine(img_obj, pc, radius, curvature=1):
    # 1 < curvature < N

    # Filter
    filter_size = 4
    filter_fct  = bicubic_fct

    # Copy input img
    tmp_img  = img_obj.copy()
    tmp_img2 = img_obj.copy()

    # Calc new coordinates
    old_coordinates = list()
    new_coordinates = list()
    for y in range(img_obj.size[1]):
        for x in range(img_obj.size[0]):
            old_coordinates.append([x,y]) 
            new_coordinates.append(spherize_coordinates((x,y,0),pc,radius,curvature))

    # X interpolation
    for i, coordinate in enumerate(new_coordinates):
        x,y = old_coordinates[i]
        x_,y_,z_ = coordinate

        # Ignore true pixel
        if type(x_) == int:
            continue

        # Get coeffs
        x_frac = x_ - int(x_)
        conv_coeffs = convolution_get_coeffs(x_frac,filter_size,filter_fct)
        conv_pixels = convolution_get_pixels(int(x_),y,img_obj,filter_size,axis="x")

        # Convolution 1d
        tmp_pixel = convolution_1d_fct(conv_coeffs,conv_pixels)
        
        # Restore alpha
        tmp_pixel = (tmp_pixel[0],tmp_pixel[1],tmp_pixel[2],img_obj.getpixel((x,y))[3])

        # Cast values
        tmp_pixel = tuple_cast(tmp_pixel)

        # Set pixel
        tmp_img.putpixel((x,y),tmp_pixel)


    # Y interpolation
    for i, coordinate in enumerate(new_coordinates):
        x,y = old_coordinates[i]
        x_,y_,z_ = coordinate

        # Ignore true pixel
        if type(y_) == int:
            continue

        # Get coeffs
        y_frac = y_ - int(y_)
        conv_coeffs = convolution_get_coeffs(y_frac,filter_size,filter_fct)
        conv_pixels = convolution_get_pixels(x,int(y_),tmp_img,filter_size,axis="y")

        # Convolution 1d
        tmp_pixel = convolution_1d_fct(conv_coeffs,conv_pixels)
        
        # Restore alpha
        tmp_pixel = (tmp_pixel[0],tmp_pixel[1],tmp_pixel[2],tmp_img.getpixel((x,y))[3])

        # Cast values
        tmp_pixel = tuple_cast(tmp_pixel)

        # Set pixel
        tmp_img2.putpixel((x,y),tmp_pixel)

    return tmp_img2