#!python3
import os, sys, math

def print_grid(array):
    for y in range(grid_size):
        for x in range(grid_size):
            x_ = int(array[x][y][0]*10)/10
            y_ = int(array[x][y][1]*10)/10
            print( '(' + str(x_) + "," + str(y_) + ")" , end="  " )
        print()

grid_size   = 11
grid_center = int(grid_size/2)
radius      = int(grid_size/2)
grid_array  = list()

# Create grid
print('###################')
print('# Create grid')
print('###################')
for x in range(grid_size):
    grid_line = list()
    for y in range(grid_size):
        grid_line.append( (x,y) )
    grid_array.append( grid_line )
print_grid(grid_array)
print()

# Calc sphere
print('###################')
print('# Calc sphere ')
print('###################')
for y in range(grid_size):
    for x in range(grid_size):

        # x = r * sin(theta) * cos(phi)
        # y = r * sin(theta) * sin(phi)
        # z = r * cos(theta)

        # r = sqrt( x^2 + y^2 + z^2 )
        # theta = acos( z / r )
        # phi = atan2 ( y / x )

        x_vec = x - grid_center
        y_vec = y - grid_center

        projected_radius = math.sqrt( x_vec**2 + y_vec**2 )

        if projected_radius < radius:

            theta = math.asin( projected_radius / radius )
            phi = math.atan2(y_vec , x_vec)
            
            # Calc new radius
            radius_ = 2 * theta * radius / math.pi

            # Calc new coordinates with new radius
            x_ = radius_ * math.sin(theta) * math.cos(phi)
            y_ = radius_ * math.sin(theta) * math.sin(phi)

            # 


            grid_array[x][y] = (x_,y_)




print()

print_grid(grid_array)
print()

