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
    ft_color2   = symbol_format[2]

    if shape == 'ellipse':
        draw.ellipse( (x,y,x+size,y+size), fill=ft_color )

    elif shape == 'cube':

        if position[1] % 2 == 0:
            draw.polygon( ( x,y+size/2,\
                            x+size/2,y,\
                            x+size/2,y+size/2,\
                            x,y+size\
                            ), fill=ft_color )

            draw.polygon( ( x+size/2,y,\
                            x+size,y+size/2,\
                            x+size,y+size,\
                            x+size/2,y+size/2\
                            ), fill=ft_color2 )
        else:
            draw.polygon( ( x,y,\
                            x+size/2,y+size/2,\
                            x+size/2,y+size,\
                            x,y+size/2\
                            ), fill=ft_color2 )

            draw.polygon( ( x+size/2,y+size/2,\
                            x+size,y,\
                            x+size,y+size/2,\
                            x+size/2,y+size\
                            ), fill=ft_color )

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


def create_all_symbol(img,shape,nb_symbol,symbol_size,symbol_color,span,mu,sig,symbol_color2=None,max_alpha=255,alpha_fct=True,inv_alpha=False,color_fct=True,inv_color=False):
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

            if symbol_color2 == None:
                tmp_symbol_color2 = tmp_symbol_color
            else:
                # Apply color_factor
                tmp_symbol_color2 =  (   symbol_color2[0]*color_factor, \
                                         symbol_color2[1]*color_factor, \
                                         symbol_color2[2]*color_factor, \
                                         alpha \
                                     )

                # Cast values
                tmp_symbol_color2 =  (   int(tmp_symbol_color2[0]), \
                                         int(tmp_symbol_color2[1]), \
                                         int(tmp_symbol_color2[2]), \
                                        alpha \
                                     )

            # Set symbol format
            symbol_format = ( symbol_size, tmp_symbol_color, tmp_symbol_color2 )

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



