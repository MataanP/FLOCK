import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import measurements
from scipy.spatial import distance_matrix


class BoidGUI:

    def __init__(self, host_info, my_boids, my_aboids):
        self.host_info = host_info
        self.speed = .5
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
        self.all_aboids = my_aboids
        self.n_l_halo = my_boids
        self.n_r_halo = my_boids
        self.boid_size = 100
        self.scat = self.ax.scatter(self.my_boids['position'], self.my_boids['position'], s=self.boid_size, lw=.5, edgecolors='none', facecolors='green', marker=">")
        self.a_scat = self.ax.scatter(self.my_aboids['position'], self.my_aboids['position'], s = self.boid_size, lw=.5, edgecolor='none', facecolors='red', marker=">")
        self.run()

    def get_data(self):
        n_birds = count(self.my_boids)
        #print(self.my_boids['position'])
        new_birds = np.zeros(n_birds, dtype=[('position', float, 2)])
        new_self.my_boids['position'] = [[.5, .2], [.1, .9], [.2, .1], [.8, .8], [.4, .5], [.9, .9], [.2, .9], [.2, .5], [.8, .1]]

        self.my_boids = new_birds
        self.my_boids['position'] = new_self.my_boids['position']

        print('boids = ')
        print(self.my_boids['position'])
        print('new_bird = ')
        print(new_self.my_boids['position'])


    def decide_move(self, i):
        dist = distance_matrix(self.my_boids['position'], self.all_aboids['position'])
        x = np.argmin(dist[i])
        if self.my_aboids['position'][x, 0] == self.my_boids['position'][i, 0] and self.my_aboids['position'][x, 1] > self.my_boids['position'][i, 1]:
            self.my_boids['position'][i, 1] += self.speed
        elif self.my_aboids['position'][x, 0] == self.my_boids['position'][i, 0] and self.my_aboids['position'][x, 1] < self.my_boids['position'][i, 1]:
            self.my_boids['position'][i, 1] -= self.speed
        elif self.my_aboids['position'][x, 1] == self.my_boids['position'][i, 1] and self.my_aboids['position'][x, 0] > self.my_boids['position'][i, 0]:
            self.my_boids['position'][i, 0] += self.speed
        elif self.my_aboids['position'][x, 1] == self.my_boids['position'][i, 1] and self.my_aboids['position'][x, 0] < self.my_boids['position'][i, 0]:
            self.my_boids['position'][i, 0] -= self.speed
            # diag axis logic
        elif self.my_boids['position'][i, 1] > self.my_aboids['position'][x, 1] and self.my_boids['position'][i, 0] > self.my_aboids['position'][x, 0]:
            self.my_boids['position'][i, 1] -= self.speed
            self.my_boids['position'][i, 0] -= self.speed
        elif self.my_boids['position'][i, 1] > self.my_aboids['position'][x, 1] and self.my_boids['position'][i, 0] < self.my_aboids['position'][x, 0]:
            self.my_boids['position'][i, 0] += self.speed
            self.my_boids['position'][i, 1] -= self.speed
        elif self.my_boids['position'][i, 1] < self.my_aboids['position'][x, 1] and self.my_boids['position'][i, 0] > self.my_aboids['position'][x, 0]:
            self.my_boids['position'][i, 1] += self.speed
            self.my_boids['position'][i, 0] -= self.speed
        elif self.my_boids['position'][i, 1] < self.my_aboids['position'][x, 1] and self.my_boids['position'][i, 0] < self.my_aboids['position'][x, 0]:
            self.my_boids['position'][i, 1] += self.speed
            self.my_boids['position'][i, 0] += self.speed

    def a_decide_move(self, i):
        centroid = np.rint(measurements.center_of_mass(self.my_boids['position']))
        if centroid[0] == self.my_aboids['position'][i, 0] and centroid[1] < self.my_aboids['position'][i, 1]:
            if self.my_aboids['position'][i,1] >= self.y_max-self.speed:
                self.my_aboids['position'][i,1] = self.y_min+self.speed
            else:
                self.my_aboids['position'][i, 1] += self.speed
        elif centroid[0] == self.my_aboids['position'][i, 0] and centroid[1] > self.my_aboids['position'][i, 1]:
            if self.my_aboids['position'][i,1] <= self.y_min+self.speed:
                self.my_aboids['position'][i,1] = self.y_max-self.speed
            else:
                self.my_aboids['position'][i, 1] -= self.speed
        elif centroid[1] == self.my_aboids['position'][i, 1] and centroid[0] < self.my_aboids['position'][i, 0]:
            self.my_aboids['position'][i, 0] += self.speed
        elif centroid[1] == self.my_aboids['position'][i, 1] and centroid[0] > self.my_aboids['position'][i, 0]:
            self.my_aboids['position'][i, 0] -= self.speed
        elif centroid[1] > self.my_aboids['position'][i, 1] and centroid[0] > self.my_aboids['position'][i, 0]:
            if self.my_aboids['position'][i,1] <= self.y_min+self.speed:
                self.my_aboids['position'][i,1] = self.y_max-self.speed
            else:
                self.my_aboids['position'][i, 1] -= self.speed
            self.my_aboids['position'][i, 0] -= self.speed
        elif centroid[1] > self.my_aboids['position'][i, 1] and centroid[0] < self.my_aboids['position'][i, 0]:
            if self.my_aboids['position'][i,1] <= self.y_min+self.speed:
                self.my_aboids['position'][i,1] = self.y_max-self.speed
            else:
                self.my_aboids['position'][i, 1] -= self.speed
            self.my_aboids['position'][i, 0] += self.speed
        elif centroid[1] < self.my_aboids['position'][i, 1] and centroid[0] > self.my_aboids['position'][i, 0]:
            if self.my_aboids['position'][i,1] >= self.y_max-self.speed:
                self.my_aboids['position'][i,1] = self.y_min+self.speed
            else:
                self.my_aboids['position'][i, 1] += self.speed
            self.my_aboids['position'][i, 0] -= self.speed
        elif centroid[1] < self.my_aboids['position'][i, 1] and centroid[0] < self.my_aboids['position'][i, 0]:
            if self.my_aboids['position'][i,1] >= self.y_max-self.speed:
                self.my_aboids['position'][i,1] = self.y_min+self.speed
            else:
                self.my_aboids['position'][i, 1] += self.speed
            self.my_aboids['position'][i, 0] += self.speed

    def push_UPD(self):
        self.host_info.my_boids = self.host_info.GUI_to_host(self.my_boids)
        self.host_info.my_aboids = self.host_info.GUI_to_host(self.my_aboids)
        self.host_info.all_aboids = self.host_info.GUI_to_host(self.all_aboids)
        self.host_info.n_l_halo = self.host_info.GUI_to_host(self.n_l_halo)
        self.host_info.n_r_halo = self.host_info.GUI_to_host(self.n_r_halo)

    def pull_UPD(self):
        self.my_boids = self.host_info.host_to_GUI(self.my_boids)
        self.my_aboids = self.host_info.host_to_GUI(self.my_aboids)
        self.all_aboids = self.host_info.host_to_GUI(self.all_aboids)
        self.n_l_halo = self.host_info.host_to_GUI(self.n_l_halo)
        self.n_r_halo = self.host_info.host_to_GUI(self.n_r_halo)

    def update(self, data):
        self.host_info.update_my_boids()
        self.pull_UPD()
        # Pick position for regular self.my_boids
        #get_data()
        print('real a_boids: ')
        print(self.my_aboids['position'])
        curr_num = len(self.my_boids['position'])
        for i in range(len(self.my_boids['position'])):
            self.decide_move(i)
        for i in range(len(self.my_aboids['position'])):
            self.a_decide_move(i)
        # Update the scatter collection, with the new position
        self.scat.set_offsets(self.my_boids['position'])
        self.a_scat.set_offsets(self.my_aboids['position'])
        self.push_UPD()

    def run(self):
        animation = FuncAnimation(self.fig, self.update, interval=10)
        plt.show()
