import numpy as np
import random
from BoidGUI import BoidGUI

class HostInfo:

	def __init__(self, min, max):
		#probably want to instantiate the boids and alpha boids within the new area inside this constructor...
		self.x_min = min
		self.x_max = max
		self.y_min = 0
		self.y_max = 50
		self.num_boids = 5
		self.num_aboids = 1
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
		self.run()

	def merge_left_backups():
		"""
		A method used to merge the left backup with our current list of birds and alphas
		"""
		left_birds = self.string_to_numpy_array(self.l_backup)
		left_alpha_birds = self.string_to_numpy_array(self.l_backup_alphas)
		self.my_boids = np.append(self.my_boids,left_birds)
		self.my_aboids = np.append(self.my_aboids,left_alpha_birds)

	def merge_right_backups():
		"""
		A method used to merge the right backup with our current list of birds and alphas
		"""
		right_birds = self.string_to_numpy_array(self.r_backup)
		right_alpha_birds = self.string_to_numpy_array(self.r_backup_alphas)
		self.my_boids = np.append(self.my_boids,right_birds)
		self.my_aboids = np.append(self.my_aboids,right_alpha_birds)

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
		"""
	    returns a tuple of numpy arrays, the first is a backup of all boids
	    in the left and the second is a backup of all boid in the right
	    """
		left_backup = np.array([])
		right_backup = np.array([])
		middle_split = int(((self.x_max-self.x_min)/2.0)+.5)
		for index in range(len(self.my_boids)):
			if self.my_boids['position'][index, 0] <= middle_split:
				np.append(left_backup, self.my_boids['position'][index])
			else:
				np.append(right_backup, self.my_boids['position'][index])
		return (self.numpy_array_to_string(left_backup),self.numpy_array_to_string(right_backup))


	def get_our_alpha_backup(self):
	    """
	    returns a tuple of numpy arrays, the first is a backup of all boids
	    in the left and the second is a backup of all boid in the right
	    """
	    left_alpha_backup = np.array([])
	    right_alpha_backup = np.array([])
	    middle_split = (self.x_max-self.x_min)/2
	    for coordinates in np.nditer(self.my_boids):
	      if coordinates[0] <=middle_split:
	        np.append(left_alpha_backup,coordinates)
	      else:
	        np.append(right_alpha_backup,coordinates)
	    return (self.numpy_array_to_string(left_alpha_backup),self.numpy_array_to_string(right_alpha_backup))


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

	def update_my_boids(self, new_my_boids):
	    """
	    Method to update my boids, should only really be accessed by the boid calculation class
	    """
	    self.my_boids = new_my_boids

	def update_my_aboids(self,new_my_aboids):
	    """
	    Method to update my Aboids, should only really be accessed by the boid calculation class
	    """
	    self.my_aboids = new_my_aboids

	def update_all_aboids(self, a_boid_string_list):
	    """
	    Method to update all a boids, should be a compilation of all a boids from host updates.
		Should receive a list of strings that are the first part of payload from each HUPD
	    """
	    numpy_array = np.array([])
	    for string in a_boid_string_list:
	      np.append(numpy_array, self.string_to_numpy_array(string))
	    self.all_aboids = numpy_array

	def create_left_halo(self):
		"""
	    separate my boids into a left halo, for boids 10 spaces away from xmin
	    """
		halo_bounday = x_min + 10
		left_halo_array = np.array([])
		for nparray in my_boids:	#ask lilly if i can do this
			if nparray[0] <= halo_boundary:
				np.append(left_halo_array, nparray)
		self.l_halo = left_halo_array

	def create_right_halo(self):
		"""
	    separate my boids into a right halo, for boids 10 spaces away from xmax
	    """
		halo_boundary = x_min - 10
		right_halo_array = np.array([])
		for nparray in np.nditer(my_boids):	#ask lilly if i can do this
			if nparray[0] >= halo_boundary:
				np.append(right_halo_array, nparray)
		self.r_halo = right_halo_array

	def string_to_numpy_array(self, array_string):
		"""
		A method that turns a string that represents a numpy Array of Arrays
		into an actual numpy Array
		"""
		comma_counter = 0
		for i in range(0,len(array_string)):# the number of smaller arrays in the total array will be equal to number of commas
			if array_string[i:i+1] == ",":
				comma_counter+=1

		array = np.zeros(comma_counter, dtype=[('position', float, 2)])# create a zero array

		array_iterator = 0 # a counter for
		current_comma = -1
		next_comma = array_string.find(",")
		next_tunnel = array_string.find("|")
		timeToStop = False
		while array_iterator<comma_counter:
			print("x int is:"+array_string [current_comma+1:next_tunnel])
			print("y int is:"+array_string [next_tunnel+1:next_comma])

			x_int = float(array_string [current_comma+1:next_tunnel])# the x coord from the string (in between current comma, and the next tunnel)
			y_int = float(array_string [next_tunnel+1:next_comma])# the y coord from the string (in between current tunnel and and next comma)
			array["position"][array_iterator,0] = x_int#[position] takes you into the x-y plane, array iterator goes through list of coordinates, 0 is x
			array["position"][array_iterator,1] = y_int# 1 is y
			current_comma = next_comma
			next_comma = array_string.find(",", next_comma+1,len(array_string)-1)
			array_iterator+=1
			next_tunnel = array_string.find("|",next_tunnel+1,len(array_string)-1)
		return array

	def numpy_array_to_string(self, numpy_array):
		position_array = numpy_array["position"]
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
