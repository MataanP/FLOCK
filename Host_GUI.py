
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import measurements

#The total distance from left to right of each host's screen
host_range = 100

#Logic for choosing left and right boundaries given a host

# x axis range is decided by the pre-existing host. x_max of host_n-1 is the x_min of host_n
# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(x_min, x_min + host_range), ax.set_xticks([])
ax.set_ylim(0, host_range), ax.set_yticks([])

# Create bird data
n_birds = birds['position'].size
a_n_birds = a_birds['position'].size
birds = np.zeros(n_birds, dtype=[('position', float, 2)])
a_birds = np.zeros(a_n_birds, dtype=[('position', float, 2)])

# Initialize the birds position
birds['position'] = [] #append np.arrays of coordinates to these arrays
a_birds['position'] = []

# Size of the birds
size = 100
# Construct the scatter which we will update during animation
scat = ax.scatter(birds['position'], birds['position'],
                  s=size, lw=.5, edgecolors='none',
                  facecolors='green', marker=">")

a_scat = ax.scatter(a_birds['position'], a_birds['position'],
                    s = size, lw=.5, edgecolor='none',
                    facecolors='red', marker=">")

def decide_move(i):
    """
    :param i: this is the ith bird's coordinates in a 1D array of birds
    :return: a change of coordinates of bird i.

    The logic runs such that if x-y movement is most efficient, it occurs first.
    Otherwise it prefers diag movement.
    """
    if birds['position'][i, 0] == a_birds['position'][0, 0] or birds['position'][i, 1] == a_birds['position'][0, 1]:
        if a_birds['position'][0, 1] > birds['position'][i, 1]:
            birds['position'][i, 1] += 0.001
        elif a_birds['position'][0, 1] < birds['position'][i, 1]:
            birds['position'][i, 1] -= 0.001
        elif a_birds['position'][0, 0] > birds['position'][i, 0]:
            birds['position'][i, 0] += 0.001
        elif a_birds['position'][0, 0] < birds['position'][i, 0]:
            birds['position'][i, 0] -= 0.001
    else:
        if birds['position'][i, 1] > a_birds['position'][0, 1] and birds['position'][i, 0] > a_birds['position'][0, 0]:
            birds['position'][i, 1] -= 0.001
            birds['position'][i, 0] -= 0.001
        elif birds['position'][i, 1] > a_birds['position'][0, 1] and birds['position'][i, 0] < a_birds['position'][0, 0]:
            birds['position'][i, 0] += 0.001
            birds['position'][i, 1] -= 0.001
        elif birds['position'][i, 1] < a_birds['position'][0, 1] and birds['position'][i, 0] > a_birds['position'][0, 0]:
            birds['position'][i, 1] += 0.001
            birds['position'][i, 0] -= 0.001
        elif birds['position'][i, 1] < a_birds['position'][0, 1] and birds['position'][i, 0] < a_birds['position'][0, 0]:
            birds['position'][i, 1] += 0.001
            birds['position'][i, 0] += 0.001

def a_decide_move():
    centroid = np.rint(measurements.center_of_mass(birds['position']))
    if centroid[0] == a_birds['position'][0, 0] and centroid[1] < a_birds['position'][0, 1]:
        a_birds['position'][0, 1] -= 0.001
    elif centroid[0] == a_birds['position'][0, 0] and centroid[1] > a_birds['position'][0, 1]:
        a_birds['position'][0, 1] += 0.001
    elif centroid[1] == a_birds['position'][0, 1] and centroid[0] < a_birds['position'][0, 0]:
        a_birds['position'][0, 0] += 0.001
    elif centroid[1] == a_birds['position'][0, 1] and centroid[0] > a_birds['position'][0, 0]:
        a_birds['position'][0, 0] -= 0.001
    elif centroid[1] > a_birds['position'][0, 1] and centroid[0] > a_birds['position'][0, 0]:
        a_birds['position'][0, 1] -= 0.001
        a_birds['position'][0, 0] -= 0.001
    elif centroid[1] > a_birds['position'][0, 1] and centroid[0] < a_birds['position'][0, 0]:
        a_birds['position'][0, 1] -= 0.001
        a_birds['position'][0, 0] += 0.001
    elif centroid[1] < a_birds['position'][0, 1] and centroid[0] > a_birds['position'][0, 0]:
        a_birds['position'][0, 1] += 0.001
        a_birds['position'][0, 0] -= 0.001
    elif centroid[1] < a_birds['position'][0, 1] and centroid[0] < a_birds['position'][0, 0]:
        a_birds['position'][0, 1] += 0.001
        a_birds['position'][0, 0] += 0.001

def update(frame_number):
    # Pick position for regular birds
    for i in range(n_birds):
        decide_move(i)
    # Generate psuedo random movements
    a_decide_move()

    # Update the scatter collection, with the new position
    scat.set_offsets(birds['position'])
    a_scat.set_offsets(a_birds['position'])



# Construct the animation, using the update function as the animation
# director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()
