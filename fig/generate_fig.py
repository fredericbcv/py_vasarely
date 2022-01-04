import numpy as np
import matplotlib.pyplot as plt
import matplotlib, math

# Create subplot
fig, ax = plt.subplots(1)

# Create circle
theta = np.linspace(0, 2*np.pi, 100)
r = 250.0
x1 = r*np.cos(theta)
x2 = r*np.sin(theta)

# Print circle
ax.plot(x1, x2)
ax.set_aspect(1)

# Configure grid
plt.xlim(-300.00,300.00)
plt.ylim(-300.00,300.00)
plt.grid(linestyle='--')
plt.xlabel('X')
plt.ylabel('Z')

# Adding points
xy1,xy2 = (-100, 0.0), (0.0,0.0)

# Create vector to translate
#ax.plot(xy1, xy2,  color='r', lw=2)
#ax.scatter(xy1[0],xy1[1], color='r')
#ax.scatter(xy2[0],xy2[1], color='r')
#ax.annotate('x', (-110,-35.0) )
#ax.annotate('x0', (-10.0,-35.0) )
#ax.annotate('r', (-50.0,15.0), color='r')

# Save file
#plt.savefig("fig_01.png", bbox_inches='tight')

# Arc de cercle
ax.annotate('r', (-80.0,250.0), color='r')
a = matplotlib.patches.Arc((0, 0), 500, 500, 0, 90, 90+(100/250)*90, color='red', lw=2, zorder=5)
ax.add_patch(a)

# Create vector to translate
x_ = 250 * math.sin( 100/250 * (math.pi/2) )

ax.plot((-1*x_,0.0), xy2,  color='orange', lw=2)
ax.annotate('r\'', (-75.0,15.0), color='orange')

ax.plot( (-1*x_,0.0), (200.0,0.0), color='black', lw=1 )
ax.plot( (0.0,0.0), (250.0,0.0), color='black', lw=1 )

b = matplotlib.patches.Arc((0, 0), 150, 150, 0, 90, 90+(100/250)*90, color='black', lw=1, zorder=5)
ax.annotate(r'$\theta$', (-40.0,100.0), color='black')
ax.add_patch(b)

#ax.plot((-100.0,-0.0), (-3.0,-3.0),  color='red', lw=2)
#ax.annotate('r', (-75.0,-35.0), color='red')

# Save file
plt.savefig("fig_02.png", bbox_inches='tight')

#plt.savefig("fig_03.png", bbox_inches='tight')


#plt.show()
