
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


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
birds['position'] = [[.5, .2], [.1, .9], [.2, .1], [.8, .8], [.4, .5]]
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
    #xy axis logic
    for i in range(n_birds):
        if a_birds['position'][0,0] == birds['position'][i, 0] and a_birds['position'][0,1] > birds['position'][i,1]:
            birds['position'][i,1] += 0.001
        elif a_birds['position'][0, 0] == birds['position'][i, 0] and a_birds['position'][0, 1] < birds['position'][i, 1]:
            birds['position'][i,1] -= 0.001
        elif a_birds['position'][0,1] == birds['position'][i, 1] and a_birds['position'][0,0] > birds['position'][i, 0]:
            birds['position'][i, 0] += 0.001
        elif a_birds['position'][0,1] == birds['position'][i, 1] and a_birds['position'][0, 0] < birds['position'][i, 0]:
            birds['position'][i, 0] -= 0.001
            #diag axis logic
        elif birds['position'][i,1] > a_birds['position'][0,1] and birds['position'][i, 0] > a_birds['position'][0, 0]:
            birds['position'][i, 1] -= 0.001
            birds['position'][i, 0] -= 0.001
        elif birds['position'][i,1] > a_birds['position'][0,1] and birds['position'][i, 0] < a_birds['position'][0, 0]:
            birds['position'][i, 0] += 0.001
            birds['position'][i, 1] -= 0.001
        elif birds['position'][i,1] < a_birds['position'][0,1] and birds['position'][i, 0] > a_birds['position'][0, 0]:
            birds['position'][i, 1] += 0.001
            birds['position'][i, 0] -= 0.001
        elif birds['position'][i,1] < a_birds['position'][0,1] and birds['position'][i, 0] < a_birds['position'][0, 0]:
            birds['position'][i, 1] += 0.001
            birds['position'][i, 0] += 0.001
    # Update the scatter collection, with the new position
    scat.set_offsets(birds['position'])


# Construct the animation, using the update function as the animation
# director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()
