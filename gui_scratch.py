
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def move_xy(boid, a_boid):
    if boid[0] == a_boid[0] and boid[1] < a_boid[1]:
        boid = move_down(boid)
    elif boid[0] == a_boid[0] and boid[1] > a_boid[1]:
        boid = move_up(boid)
    elif boid[1] == a_boid[1] and boid[0] < a_boid[0]:
        boid = move_right(boid)
    elif boid[1] == a_boid[1] and boid[0] > a_boid[0]:
        boid = move_left(boid)

#Split the diag movement to its own logic check
def move_diag(boid, a_boid):
    if boid[1] > a_boid[1] and boid[0] > a_boid[0]:
        boid = move_bot_left(boid)
    elif boid[1] > a_boid[1] and boid[0] < a_boid[0]:
        boid = move_bot_right(boid)
    elif boid[1] < a_boid[1] and boid[0] > a_boid[0]:
        boid = move_top_left(boid)
    elif boid[1] < a_boid[1] and boid[0] < a_boid[0]:
        boid = move_top_right(boid)

#Decide the most efficient move based on coordinates
def decide_move(boid, a_boid):
    if boid[0] == a_boid[0] or boid[1] == a_boid[1]:
        move_xy(boid, a_boid)
    else:
        move_diag(boid, a_boid)

steps = .001
#horizontal/vertical movements
#x coordinate postive shift, no y shift
def move_right(arr):
    arr[0] += steps

#x coordinate negative shift, no y shift
def move_left(arr):
    arr[0] -= steps

#no x shift, y coordinate positive shift
def move_up(arr):
    arr[1] += steps

#no x shift, y coordinate negative shift
def move_down(arr):
    arr[1] -= steps


#diagnoal movements
def move_top_right(arr):
    arr[0] += steps
    arr[1] += steps

def move_top_left(arr):
    arr[0] -= steps
    arr[1] += steps

def move_bot_left(arr):
    arr[0] -= steps
    arr[1] -= steps

def move_bot_right(arr):
    arr[0] += steps
    arr[1] -= steps

# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1), ax.set_xticks([])
ax.set_ylim(0, 1), ax.set_yticks([])

# Create bird data
n_birds = 5
a_n_birds = 1
birds = np.zeros(n_birds, dtype=[('position', float, 2)])
a_birds = np.zeros(a_n_birds, dtype=[('position', float, 2)])

# Initialize the birds position
birds['position'] = [[.4, .2], [.1, .2], [.4, .5], [.8, .1], [.4, .2]]
a_birds['position'] = [[.5, .5]]

# Construct the scatter which we will update during animation
scat = ax.scatter(birds['position'], birds['position'],
                  s=30, lw=.5, edgecolors='none',
                  facecolors='green', marker=">")

a_scat = ax.scatter(a_birds['position'], a_birds['position'],
                    s = 30, lw=.5, edgecolor='none',
                    facecolors='red', marker=">")

def update(frame_number):
    # Pick a new position for birds
    #move right
    birds['position'][:,0] += 0.001

    # Update the scatter collection, with the new position
    scat.set_offsets(birds['position'])
    print(birds['position'][:,0])

# Construct the animation, using the update function as the animation
# director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()
