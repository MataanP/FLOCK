import numpy as np
import random
from BoidGUI import BoidGUI

class HostInfo:

	def __init__(self, min, max):
		self.alone = True
		self.x_min = min
		self.x_max = max
		self.y_min = 0
		self.y_max = 50
		self.num_boids = 10
		self.num_aboids = 2
		self.my_boids = np.array([]) # READ HERE,initializes an empty numpy array. When adding boids: np.append(my_boids,np.array([x,y]))
		self.my_aboids = np.array([])
		self.all_aboids = np.array([])
		self.n_l_halo = np.array([])
		self.n_r_halo = np.array([])
		self.l_halo = np.array([])
		self.r_halo = np.array([])
		self.l_backup_alphas=''
		self.r_backup_alphas=''
		self.l_backup = ''
		self.r_backup = ''
		self.l_neighbor_ip = ''
		self.r_neighbor_ip = ''
		self.running = True
		print('about to run')

	def merge_halos(self):
		num_total = self.my_boids.size + self.n_l_halo.size + self.n_r_halo.size
		total_boids = np.zeros(num_total, dtype=[('position', float, 2)])
		index = 0
		for i in range(self.my_boids.size):
			total_boids['position'][index] = self.my_boids['position'][i]
			index += 1
		for i in range(self.n_l_halo.size):
			total_boids['position'][index] = self.n_l_halo['position'][i]
			index += 1
		for i in range(self.n_r_halo.size):
			total_boids['position'][index] = self.n_r_halo['position'][i]
			index += 1
		self.my_boids = total_boids


	def merge_left_backups(self):
		"""
		A method used to merge the left backup with our current list of birds and alphas
		"""
		num_left = self.my_boids.size + self.l_backup.size
		num_left_alpha = self.my_aboids.size + self.l_backup_alphas.size

		left = np.zeros(num_left, dtype=[('position', float, 2)])
		left_alpha = np.zeros(num_left_alpha, dtype=[('position', float, 2)])

		left_index = 0
		left_alpha_index = 0

		for i in range(self.my_boids.size):
			left['position'][left_index] = self.my_boids['position'][i]
			left_index += 1
		for i in range(self.l_backup.size):
			left['position'][left_index] = self.l_backup['position'][i]
			left_index += 1

		for i in range(self.my_aboids.size):
			left_alpha['position'][left_alpha_index] = self.my_aboids['position'][i]
			left_alpha_index += 1
		for i in range(self.l_backup_alphas.size):
			left_alpha['position'][left_alpha_index] = self.l_backup_alphas['position'][i]
			left_alpha_index += 1

		left_birds = self.string_to_numpy_array(self.l_backup)
		left_alpha_birds = self.string_to_numpy_array(self.l_backup_alphas)
		self.my_boids = left
		self.my_aboids = left_alpha


	def merge_right_backups(self):
		"""
		A method used to merge the right backup with our current list of birds and alphas
		"""
		num_right = self.my_boids.size + self.r_backup.size
		num_right_alpha = self.my_aboids.size + self.r_backup_alphas.size

		right = np.zeros(num_right, dtype=[('position', float, 2)])
		right_alpha = np.zeros(num_right_alpha, dtype=[('position', float, 2)])

		right_index = 0
		right_alpha_index = 0

		for i in range(self.my_boids.size):
			right['position'][right_index] = self.my_boids['position'][i]
			right_index += 1
		for i in range(self.r_backup.size):
			right['position'][right_index] = self.r_backup['position'][i]
			right_index += 1

		for i in range(self.my_aboids.size):
			right_alpha['position'][right_alpha_index] = self.my_aboids['position'][i]
			right_alpha_index += 1
		for i in range(self.r_backup_alphas.size):
			right_alpha['position'][right_alpha_index] = self.r_backup_alphas['position'][i]
			right_alpha_index += 1

		self.my_boids = right
		self.my_aboids = right_alpha

	def host_to_GUI(self, list):
		templist = list
		for i in range(len(list)):
		    templist['position'][i,0] = list['position'][i,0] - self.x_min
		return templist

	def GUI_to_host(self, list):
		templist = list
		for i in range(len(list)):
		    templist['position'][i,0] = list['position'][i,0] + self.x_min
		return templist


	def instantiate_our_boids(self):
		"""
		instantiates all the my_boids and my_aboids
		"""
		boids = np.zeros(self.num_boids, dtype=[('position', float, 2)])
		aboids = np.zeros(self.num_aboids, dtype=[('position', float, 2)])
		temp_boids = []
		temp_aboids = []
		i = self.num_boids
		while i > 0:
		    x = random.randint(self.x_min, self.x_max)
		    y = random.randint(self.y_min, self.y_max)
		    new_boid = [x, y]
		    temp_boids.append(new_boid)
		    i -= 1;
		i = self.num_aboids
		while i > 0:
		    x = random.randint(self.x_min, self.x_max)
		    y = random.randint(self.y_min, self.y_max)
		    new_a_boid = [x, y]
		    temp_aboids.append(new_a_boid)
		    i-= 1
		boids['position'] = temp_boids
		aboids['position'] = temp_aboids
		self.my_boids = boids
		self.my_aboids = aboids

	def get_our_backup(self):
		num_left = 0
		num_right = 0
		middle_split = int(((self.x_max-self.x_min)/2.0)+.5) + self.x_min
		for i in range(self.my_boids.size):
			if middle_split > self.my_boids['position'][i, 0] and self.x_min <= self.my_boids['position'][i, 0]:
				num_left += 1
			elif middle_split < self.my_boids['position'][i, 0] and self.x_max >= self.my_boids['position'][i, 0]:
				num_right += 1
			else:
				np.delete(self.my_boids, self.my_boids['position'][i])
		print('num left  = ' + str(num_left))
		print('num right = ' + str(num_right))

		left_backup = np.zeros(num_left, dtype=[('position', float, 2)])
		right_backup = np.zeros(num_right, dtype=[('position', float, 2)])
		left_index = 0
		right_index = 0

		for i in range(num_left + num_right):
			print('left index is at ' + str(left_index))
			print('right index is at ' + str(right_index))
			if middle_split > self.my_boids['position'][i, 0] and self.x_min <= self.my_boids['position'][i, 0]:
				left_backup['position'][left_index] = self.my_boids['position'][i]
				left_index += 1
			elif middle_split < self.my_boids['position'][i, 0] and self.x_max >= self.my_boids['position'][i, 0]:
				right_backup['position'][right_index] = self.my_boids['position'][i]
				right_index += 1

		return (self.numpy_array_to_string(left_backup),self.numpy_array_to_string(right_backup))


	def get_our_alpha_backup(self):
		"""
		returns a tuple of numpy arrays, the first is a backup of all boids
		in the left and the second is a backup of all boid in the right
		"""
		num_left = 0
		num_right = 0
		middle_split = int(((self.x_max-self.x_min)/2.0)+.5) + self.x_min
		for i in range(self.my_aboids.size):
			if middle_split > self.my_aboids['position'][i, 0]:
				num_left += 1
			else:
				num_right += 1

		left_backup = np.zeros(num_left, dtype=[('position', float, 2)])
		right_backup = np.zeros(num_right, dtype=[('position', float, 2)])
		left_index = 0
		right_index = 0

		for i in range(self.my_aboids.size):
			if middle_split > self.my_aboids['position'][i, 0]:
				left_backup['position'][left_index] = self.my_aboids['position'][i]
				left_index += 1
			else:
				right_backup['position'][right_index] = self.my_aboids['position'][i]
				right_index += 1

		return (self.numpy_array_to_string(left_backup),self.numpy_array_to_string(right_backup))



	def update_n_l_halo(self, string_of_halo):
		"""
		A method that updates the halo given to us by the left host, retrieved as payload in HUPD
		"""
		halo_array = self.string_to_numpy_array(string_of_halo)
		self.n_l_halo = halo_array

	def update_n_r_halo(self, string_of_halo):
		"""
		A method that updates the halo given to us by the right host, retrieved as payload in HUPD
		"""
		halo_array = self.string_to_numpy_array(string_of_halo)
		self.n_r_halo = halo_array

	def update_my_boids(self):
		"""
		Method to update my boids, should only really be accessed by the boid calculation class
		"""
		#check if birds from left neighbor's right half came into my range
		#check if birds from right neighbor's left half came into my range
		#if true, add to my birds
		if self.alone == True:
			for index in range(self.my_boids.size):
				if self.my_boids['position'][index, 0] <= self.x_min:
					self.my_boids['position'][index, 0] = self.x_max
				if self.my_boids['position'][index, 0] >= self.x_max:
					self.my_boids['position'][index, 0] = self.x_min
			for index in range(self.my_aboids.size):
				if self.my_aboids['position'][index, 0] <= self.x_min:
					self.my_aboids['position'][index, 0] = self.x_max
				if self.my_aboids['position'][index, 0] >= self.x_max:
					self.my_aboids['position'][index, 0] = self.x_min
		else:
			for index in range(self.my_boids.size):
				if self.my_boids['position'][index, 0] < self.x_min - .5 or self.my_boids['position'][index, 0] > self.x_max + .5:
					self.my_boids = np.delete(self.my_boids, self.my_boids['position'][index])
			for index in range(self.l_backup.size):
				if self.l_backup['position'][index, 0] > self.x_min and self.l_backup['position'][index, 0] < self.x_max:
					self.my_boids = self.append_single(self.my_boids, self.l_backup['position'][index])
				if self.r_backup['position'][index, 0] > self.x_min and self.r_backup['position'][index, 0] < self.x_max:
					self.my_boids = self.append_single(self.my_boids, self.r_backup['position'][index])
			for index in range(self.l_backup_alphas.size):
				if self.l_backup_alphas['position'][index, 0] > self.x_min and self.l_backup_alphas['position'][index, 0] < self.x_max:
					self.my_aboids = self.append_single(self.my_aboids, self.l_backup_alphas['position'][index])
				if self.r_backup_alphas['position'][index, 0] > self.x_min and self.r_backup_alphas['position'][index, 0] < self.x_max:
					self.my_aboids = self.append_single(self.my_aboids, self.r_backup_alphas['position'][index])

	def append(self, nparray1, nparray2):

		new_size = nparray1.size + nparray2.size
		new_array = np.zeros(new_size, typed=[('position', float, 2)])
		counter = 0
		for i in range(nparray1.size):
			new_array['position'][counter] = nparray1['position'][i]
			counter += 1
		for i in range(nparray2.size):
			new_array['position'][counter] = nparray2['position'][i]

		return new_array

	def append_single(self, nparray1, nparray_object):

		new_size = nparray1.size +1
		new_array = np.zeros(new_size, typed=[('position', float, 2)])
		counter = 0
		for i in range(nparray1.size):
			new_array['position'][counter] = nparray1['position'][i]
			counter += 1
		new_array['position'][counter] = nparray_object

		return new_array

	def update_my_aboids(self):
		"""
		Method to update my Aboids, should only really be accessed by the boid calculation class
		"""
		counter = 0

		for index in range(self.my_aboids.size):
			if self.my_aboids["position"][index,0]>=self.x_min or self.my_aboids["position"][index,0]<=self.x_max:
				counter += 1
		temp = np.zeros(counter, dtype=[('position', float, 2)])
		temp_index = 0

		for i in range(self.my_aboids.size):
			if self.my_aboids["position"][index,0]>=self.x_min or self.my_aboids["position"][index,0]<=self.x_max:
				temp['position'][temp_index] = self.my_aboids['position'][i]
				temp_index += 1

		self.my_aboids = temp

	def update_all_aboids(self, a_boid_string_list):
		"""
		Method to update all a boids, should be a compilation of all a boids from host updates.
		Should receive a list of strings that are the first part of payload from each HUPD
		"""
		temp_array = self.string_to_numpy_array(','.join(a_boid_string_list))
		num_alphas = self.my_aboids.size + temp_array.size

		alphas = np.zeros(num_alphas, dtype=[('position', float, 2)])
		alphas_index = 0

		for i in range(self.my_aboids.size):
			alphas['position'][alphas_index] = self.my_aboids['position'][i]
			alphas_index += 1
		for i in range(temp_array.size):
			alphas['position'][alphas_index] = temp_array['position'][i]
			alphas_index += 1
		self.all_aboids = alphas

		counter = 0

		for i in range(self.all_aboids.size):
			if self.all_aboids['position'][i, 0] > self.x_min and self.all_aboids['position'][i, 0] < self.x_max:
				counter += 1

		my_aboids = np.zeros(counter, dtype=[('position', float, 2)])

		counter = 0
		for i in range(self.all_aboids.size):
			if self.all_aboids['position'][i, 0] > self.x_min and self.all_aboids['position'][i, 0] < self.x_max:
				my_aboids['position'][counter] = self.all_aboids['position'][i]
				counter += 1
		self.my_aboids = my_aboids


	def create_left_halo(self):
		"""
		separate my boids into a left halo, for boids 10 spaces away from xmin
		"""
		halo_boundary = self.x_min + 10
		num_halo = 0
		for i in range(self.my_boids.size):
			if halo_boundary >= self.my_boids['position'][i, 0] and self.x_min <= self.my_boids['position'][i, 0]:
				num_halo += 1

		left_halo = np.zeros(num_halo, dtype=[('position', float, 2)])
		halo_index = 0

		for i in range(self.my_boids.size):
			if halo_boundary >= self.my_boids['position'][i, 0] and self.x_min <= self.my_boids['position'][i, 0]:
				left_halo['position'][halo_index, 0] = self.my_boids['position'][i, 0]
				halo_index += 1

		self.l_halo = left_halo

	def create_right_halo(self):
		"""
		separate my boids into a right halo, for boids 10 spaces away from xmax
		"""
		halo_boundary = self.x_max - 10
		num_halo = 0
		for i in range(self.my_boids.size):
			if halo_boundary <= self.my_boids['position'][i, 0] and self.x_max >= self.my_boids['position'][i, 0]:
				num_halo += 1
		right_halo = np.zeros(num_halo, dtype=[('position', float, 2)])
		halo_index = 0
		for i in range(self.my_boids.size):
			if halo_boundary <= self.my_boids['position'][i, 0] and self.x_max >= self.my_boids['position'][i, 0]:
				right_halo['position'][halo_index, 0] = self.my_boids['position'][i, 0]
				halo_index += 1
		self.r_halo = right_halo

	def string_to_numpy_array(self, array_string):
		"""
		A method that turns a string that represents a numpy Array of Arrays
		into an actual numpy Array
		"""
		array_string_array = array_string.split(',')
		num_birds = len(array_string_array)
		birds = np.zeros(num_birds, dtype=[('position', float, 2)])# create a zero array
		for i in range(num_birds):
			print(array_string_array[i])
			split = str(array_string_array[i]).split('|')
			if(len(split) > 1):
				print(split[0])
				print(split[1])
				x = int(split[0].split('.')[0])
				y = int(split[1].split('.')[0])
				birds['position'][i, 0] = float(x)
				birds['position'][i, 1] = float(y)
		return birds


	def numpy_array_to_string(self, numpy_array):
		position_array = numpy_array['position']
		string_to_send = ""
		for i in range(len(position_array)):
		    x = position_array[i,0]
		    y = position_array[i,1]
		    string_to_send+=str(x)+"|"+str(y)+","
		return string_to_send

	def run(self):
		print('Starting GUI')
		self.instantiate_our_boids()
		self.gui = BoidGUI(self, self.my_boids, self.my_aboids)
