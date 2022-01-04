#!python3
import math
import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as mp

################################
# IMAGE
################################
def create_image(img_size,img_color):
    return Image.new('RGBA', img_size, img_color)

################################
# GAUSSIAN
################################
def gaussian_fct(x,mu,sig):
    #return np.exp(-np.power(x - mu, 2.)/(2 * np.power(sig,2))) / ( sig*np.sqrt(2*np.pi) )
    return np.exp(-np.power(x - mu, 2.)/(2 * np.power(sig/4,2)))

    #x_values = np.linspace(0,nb_symbol[0],120)
    #mp.plot(x_values, gaussian_fct(x_values,mu,sig))
    #mp.show()

def gaussian_2d_fct(img_obj,symbol_size,mu,sig,max_alpha=255,inv_fct=False):
    img_size = img_obj.size

    for y in range(img_size[1]):
        for x in range(img_size[0]):
            x_ = int(x/symbol_size[0])*symbol_size[0]
            y_ = int(y/symbol_size[1])*symbol_size[1]

            # Calc alpha
            if y_ < (img_size[1]/2):
                if x_ >= y_ and x_ < img_size[0]-y_:
                    alpha = gaussian_fct(y_,mu,sig)
                else:
                    alpha = gaussian_fct(x_+symbol_size[0]/2,mu,sig)
            else:
                if x_ >= img_size[1]-y_-symbol_size[1] and x_ < img_size[0]-(img_size[1]-symbol_size[1]-y_):
                    alpha = gaussian_fct(img_size[1]-symbol_size[1]-y_,mu,sig)
                else:
                    alpha = gaussian_fct(x_+symbol_size[0]/2,mu,sig)

            if inv_fct:
                alpha = 1-alpha

            alpha = int(alpha*max_alpha)

            # Set new pixel
            if img_obj.getpixel((x,y))[3] > 0:
                tmp_pixel = ( img_obj.getpixel((x,y))[0],img_obj.getpixel((x,y))[1],img_obj.getpixel((x,y))[2],alpha )
                img_obj.putpixel((x,y),tmp_pixel)

################################
# SYMBOL
################################
def create_symbol(size,colors,shape):
    # Create return img
    ret_img = create_image(size,(0,0,0,0))
    # Create draw
    draw = ImageDraw.Draw(ret_img)
    # Set max size
    max_x = size[0]-1
    max_y = size[1]-1

    # Draw shape
    if shape == 'ellipse':
        draw.ellipse( (0,0,max_x,max_y), fill=colors[0] )
    elif shape == 'rectangle':
        draw.rectangle( (0,0,max_x,max_y), fill=colors[0] )
    elif shape == 'cube':
        draw.polygon( ( 0,                  int(max_y/4),\
                        int(max_x/2),       0,\
                        int(max_x/2),       int(max_y/4)+1,\
                        0,                  int(max_y/2)\
                        ), fill=colors[0] )
        draw.polygon( ( int(max_x/2)+1,     0,\
                        max_x,              int(max_y/4),\
                        max_x,              int(max_y/2),\
                        int(max_x/2)+1,     int(max_y/4)+1\
                        ), fill=colors[1] )
        draw.polygon( ( 0,                  int(max_y/2)+1,\
                        int(max_x/2),       int(max_y*3/4),\
                        int(max_x/2),       max_y,\
                        0,                  int(max_y*3/4)+1\
                        ), fill=colors[1] )
        draw.polygon( ( int(max_x/2)+1,     int(max_y*3/4),\
                        max_x,              int(max_y/2)+1,\
                        max_x,              int(max_y*3/4)+1,\
                        int(max_x/2)+1,     max_y\
                        ), fill=colors[0] )
    else:
        print('Warning(create_symbol): Unknown shape drawing ignored')

    return ret_img

def fill_image_with_symbol(img_obj,symbol_obj):
    img_size = img_obj.size
    symbol_size = symbol_obj.size
    nb_symbol = ( int(img_size[0]/symbol_size[0]) , int(img_size[1]/symbol_size[1]) )

    for y in range(nb_symbol[1]):
        for x in range(nb_symbol[0]):
            # Paste symbol
            img_obj.paste(symbol_obj,(x*symbol_size[0],y*symbol_size[1]))

def create_all_symbol(img,shape,nb_symbol,symbol_size,symbol_color,span,mu,sig,symbol_color2=None,max_alpha=255,alpha_fct=True,inv_alpha=False,color_fct=True,inv_color=False):
    draw = ImageDraw.Draw(img)
    #max_alpha = 230     # 192

    for y in range(nb_symbol[1]):
        for x in range(nb_symbol[0]):

            # Set alpha
            if alpha_fct:
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

