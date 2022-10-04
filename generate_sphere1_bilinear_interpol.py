#!python3
import inspect 
from numpy import *
from lib_symbol import *
from lib_interpolate import *

out_dir = "output/"
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

#########################
# FUNCTIONS
#########################
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

# Create img
bg_img      = create_image(img_size,(154,185,183,255))
overlay_img = create_image(img_size,(255,255,255,0))

# Create symbol
symbol_size = (50,100)
symbol_color1 = (242,198,27)
symbol_color2 = (5,26,104)
symbol_colors = ( symbol_color1 , symbol_color2 )
symbol_img   = create_symbol(symbol_size,symbol_colors,'cube')
symbol_img.save(out_dir+'symbol.png')

# Fill img with symbol
fill_image_with_symbol(overlay_img,symbol_img)

# Apply background to overlay
overlay_img = Image.alpha_composite( create_image(img_size,(0,0,0,255)), overlay_img)
overlay_img.save(out_dir+'overlay.png')

# Merge background and overlay
bg_img = Image.alpha_composite(bg_img,overlay_img)
bg_img.save(out_dir+'sphere.png')

#########################
# Sphere calc
#########################
new_img = bg_img
#new_img = sphere_engine(new_img, img_size, (0,             0             ,0), img_size[0]/2 * 2**0.5, 1.5)
#new_img = sphere_engine(new_img, img_size, (img_size[0]-1, 0             ,0), img_size[0]/2, 1.5)
#new_img = sphere_engine(new_img, img_size, (img_size[0]-1, img_size[1]-1 ,0), img_size[0]/2 * 2**0.5, 1.5)
#new_img = sphere_engine(new_img, img_size, (0,             img_size[1]-1 ,0), img_size[0]/2, 1.5)
new_img = sphere_engine(new_img, img_size, (img_size[0]/2, img_size[1]/2 ,0), img_size[0]/2, 1)

new_img.save(out_dir+'sphere1_bilinear_interpol.png')

