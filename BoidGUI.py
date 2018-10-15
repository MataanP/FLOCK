import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import measurements


class BoidGUI:

    def __init__(self, host_info, my_boids, my_aboids):
        self.host_info = host_info
        self.x_min = 0
        self.x_max = 50
        self.y_min = 0
        self.y_max = 50
        self.range = 50
        self.fig = plt.figure(figsize=(7, 7))
        self.ax = self.fig.add_axes([0, 0, 1, 1], frameon=False)
        self.ax.set_xlim(self.x_min, self.x_min + self.range), self.ax.set_xticks([])
        self.ax.set_ylim(0, self.range), self.ax.set_yticks([])
        self.num_boids = len(my_boids)
        self.num_aboids = len(my_aboids)
        self.my_boids = my_boids
        self.my_aboids = my_aboids
        self.boid_size = 100
        self.scat = self.ax.scatter(self.my_boids['position'], self.my_boids['position'], s=self.boid_size, lw=.5, edgecolors='none', facecolors='green', marker=">")
        self.a_scat = self.ax.scatter(self.my_aboids['position'], self.my_aboids['position'], s = self.boid_size, lw=.5, edgecolor='none', facecolors='red', marker=">")
        self.run()

    def get_data(self):
        n_birds = count(self.my_boids)
        #print(self.my_boids['position'])
        new_birds = np.zeros(n_birds, dtype=[('position', float, 2)])
        new_birds['position'] = [[.5, .2], [.1, .9], [.2, .1], [.8, .8], [.4, .5], [.9, .9], [.2, .9], [.2, .5], [.8, .1]]

        self.my_boids = new_birds
        self.my_boids['position'] = new_birds['position']

        print('boids = ')
        print(self.my_boids['position'])
        print('new_bird = ')
        print(new_birds['position'])


    def decide_move(self, i):
        if self.my_aboids['position'][0, 0] == self.my_boids['position'][i, 0] and self.my_aboids['position'][0, 1] > self.my_boids['position'][i, 1]:
            self.my_boids['position'][i, 1] += .1
        elif self.my_aboids['position'][0, 0] == self.my_boids['position'][i, 0] and self.my_aboids['position'][0, 1] < self.my_boids['position'][i, 1]:
            self.my_boids['position'][i, 1] -= .1
        elif self.my_aboids['position'][0, 1] == self.my_boids['position'][i, 1] and self.my_aboids['position'][0, 0] > self.my_boids['position'][i, 0]:
            self.my_boids['position'][i, 0] += .1
        elif self.my_aboids['position'][0, 1] == self.my_boids['position'][i, 1] and self.my_aboids['position'][0, 0] < self.my_boids['position'][i, 0]:
            self.my_boids['position'][i, 0] -= .1
            # diag axis logic
        elif self.my_boids['position'][i, 1] > self.my_aboids['position'][0, 1] and self.my_boids['position'][i, 0] > self.my_aboids['position'][0, 0]:
            self.my_boids['position'][i, 1] -= .1
            self.my_boids['position'][i, 0] -= .1
        elif self.my_boids['position'][i, 1] > self.my_aboids['position'][0, 1] and self.my_boids['position'][i, 0] < self.my_aboids['position'][0, 0]:
            self.my_boids['position'][i, 0] += .1
            self.my_boids['position'][i, 1] -= .1
        elif self.my_boids['position'][i, 1] < self.my_aboids['position'][0, 1] and self.my_boids['position'][i, 0] > self.my_aboids['position'][0, 0]:
            self.my_boids['position'][i, 1] += .1
            self.my_boids['position'][i, 0] -= .1
        elif self.my_boids['position'][i, 1] < self.my_aboids['position'][0, 1] and self.my_boids['position'][i, 0] < self.my_aboids['position'][0, 0]:
            self.my_boids['position'][i, 1] += .1
            self.my_boids['position'][i, 0] += .1

    def a_decide_move(self):
        centroid = np.rint(measurements.center_of_mass(self.my_boids['position']))
        if centroid[0] == self.my_aboids['position'][0, 0] and centroid[1] < self.my_aboids['position'][0, 1]:
            self.my_aboids['position'][0, 1] -= .1
        elif centroid[0] == self.my_aboids['position'][0, 0] and centroid[1] > self.my_aboids['position'][0, 1]:
            self.my_aboids['position'][0, 1] += .1
        elif centroid[1] == self.my_aboids['position'][0, 1] and centroid[0] < self.my_aboids['position'][0, 0]:
            self.my_aboids['position'][0, 0] += .1
        elif centroid[1] == self.my_aboids['position'][0, 1] and centroid[0] > self.my_aboids['position'][0, 0]:
            self.my_aboids['position'][0, 0] -= .1
        elif centroid[1] > self.my_aboids['position'][0, 1] and centroid[0] > self.my_aboids['position'][0, 0]:
            self.my_aboids['position'][0, 1] -= .1
            self.my_aboids['position'][0, 0] -= .1
        elif centroid[1] > self.my_aboids['position'][0, 1] and centroid[0] < self.my_aboids['position'][0, 0]:
            self.my_aboids['position'][0, 1] -= .1
            self.my_aboids['position'][0, 0] += .1
        elif centroid[1] < self.my_aboids['position'][0, 1] and centroid[0] > self.my_aboids['position'][0, 0]:
            self.my_aboids['position'][0, 1] += .1
            self.my_aboids['position'][0, 0] -= .1
        elif centroid[1] < self.my_aboids['position'][0, 1] and centroid[0] < self.my_aboids['position'][0, 0]:
            self.my_aboids['position'][0, 1] += .1
            self.my_aboids['position'][0, 0] += .1

    def update(self, data):
        # Pick position for regular self.my_boids
        #get_data()
        print('real self.my_boids: ')
        print(self.my_boids['position'])
        curr_num = len(self.my_boids['position'])
        for i in range(curr_num):
            self.decide_move(i)
        self.a_decide_move()
        # Update the scatter collection, with the new position
        self.scat.set_offsets(self.my_boids['position'])
        self.a_scat.set_offsets(self.my_aboids['position'])

    def run(self):
        animation = FuncAnimation(self.fig, self.update, interval=10)
        plt.show()
