
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1), ax.set_xticks([])
ax.set_ylim(0, 1), ax.set_yticks([])

# Create bird data
n_birds = 1000
birds = np.zeros(n_birds, dtype=[('position', float, 2)])


# Initialize the birds position
birds['position'] = np.random.rand(n_birds, 2)


# Construct the scatter which we will update during animation
scat = ax.scatter(birds['position'][:, 0], birds['position'][:, 1],
                  s=5, lw=.5, edgecolors='black',
                  facecolors='none')

def update(frame_number):
    # Pick a new position for birds
    birds['position'] = np.random.rand(n_birds, 2)
    # Update the scatter collection, with the new position
    scat.set_offsets(birds['position'])


# Construct the animation, using the update function as the animation
# director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()
