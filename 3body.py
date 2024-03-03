import numpy as np
import pandas as pd
from random import choice
from string import ascii_lowercase

import matplotlib.pyplot as plt
import matplotlib.animation as animation

g = -9.81

class body:
    
    def __init__(self, 
                 position = [0.,0.,0.], 
                 velocity = [0.,0.,0.], 
                 mass = 1) -> None:
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.mass = mass
        
        self.id = ''.join(choice(ascii_lowercase) for _ in range(5))
        
    def update(self, dv):
        self.velocity += 0.05*dv
        self.position += 0.05*self.velocity

def accelerate(p1, p2, p3, g = 9.81):
    a1 = -g*np.sum([p.mass*np.divide((p1.position - p.position),np.linalg.norm(p1.position - p.position)) for p in [p2, p3]],
                   axis = 0)
    a2 = -g*np.sum([p.mass*np.divide((p2.position - p.position),np.linalg.norm(p2.position - p.position)) for p in [p3, p1]],
                   axis = 0)
    a3 = -g*np.sum([p.mass*np.divide((p3.position - p.position),np.linalg.norm(p3.position - p.position)) for p in [p1, p2]],
                   axis = 0)
    
    return a1, a2, a3 


p1 = body([1.,0.,10.],[0.,0.,0.],1.)
p2 = body([10.,-1.,0.],[0.,0.,0.],2.)
p3 = body([1.,10.,-10.],[0.,0.,0.],1.3)

fig = plt.figure(frameon=False)
fig.set_size_inches(5,5)
ax = fig.add_subplot(projection='3d')
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace = 0, wspace = 0)
scat = ax.scatter([p.position[0] for p in [p1,p2,p3]],
                  [p.position[1] for p in [p1,p2,p3]],
                  [p.position[2] for p in [p1,p2,p3]],
                  c = ['darkorange','skyblue','darkseagreen'], 
                  alpha = 0.5,
                  s = [p.mass*10 for p in [p1,p2,p3]])

ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

zoom = 20
ax.set(xlim=[-zoom, zoom], ylim=[-zoom, zoom], zlim=[-zoom,zoom], xlabel='', ylabel='', zlabel='')

def update(frame):
    
    dv_1, dv_2, dv_3 = accelerate(p1,p2,p3)
    p1.update(dv_1)
    p2.update(dv_2)
    p3.update(dv_3)
    
    # update the scatter plot:
    scat._offsets3d = ([p.position[0] for p in [p1,p2,p3]],
                       [p.position[1] for p in [p1,p2,p3]],
                       [p.position[2] for p in [p1,p2,p3]])
    
    return (scat)

plt.margins(0,0,0)
ani = animation.FuncAnimation(fig=fig, func=update, frames=600, interval=50)
ax.view_init(elev=5, azim=10, roll=0)
# plt.show()

ani.save(filename="Downloads/3body_example.gif", writer="pillow", dpi=300)