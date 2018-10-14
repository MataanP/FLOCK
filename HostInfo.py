import numpy as np
class HostInfo:


	def __init__(self, min, max):
  	self.x_min = min
    self.x_max = max
    self.my_boids = np.array([]) # READ HERE,initializes an empty numpy array. When adding boids: np.append(my_boids,np.array([x,y]))
    self.my_aboids = np.array([])
    self.all_aboids = np.array([])
    self.n_l_halo = np.array([])
    self.n_r_halo = np.array([])
    self.l_halo = np.array([])
    self.r_halo = np.array([])
    self.l_backup = np.array([])
    self.r_backup = np.array([])
    self.l_neighbor_ip = ''
    self.r_neighbor_ip = ''

  def processUpdate(self, message):
    update_origin = message.origin
    update_payload = message.payload
    #we need to determine if the message comes from one of our neighbors

	def get_our_backup(self):
    """
    returns a tuple of numpy arrays, the first is a backup of all boids
    in the left and the second is a backup of all boid in the right
    """
    left_backup = np.array([])
    right_backup = np.array([])
    middle_split = (x_max-x_min)/2
    for coordinates in np.nditer(my_boids):
      if coordinates[0] <=middle_split:
        np.append(left_backup,coordinates)
      else:
        np.append(right_backup,coordinates)
    return (self.numpy_array_to_string(left_backup),self.numpy_array_to_string(right_backup))

  def get_our_alpha_backup(self):
    """
    returns a tuple of numpy arrays, the first is a backup of all boids
    in the left and the second is a backup of all boid in the right
    """
    left_alpha_backup = np.array([])
    right_alpha_backup = np.array([])
    middle_split = (x_max-x_min)/2
    for coordinates in np.nditer(my_boids):
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
    n_l_halo = halo_array

  def update_n_r_halo(self, string_of_halo):
    """
    A method that updates the halo given to us by the right host, retrieved as payload in HUPD
    """
    halo_array = self.string_to_numpy_array(string_of_halo)
    n_r_halo = halo_array

  def update_my_boids(self, new_my_boids):
    """
    Method to update my boids, should only really be accessed by the boid calculation class
    """
    my_boids = new_my_boids

  def update_my_aboids(self,new_my_aboids):
    """
    Method to update my Aboids, should only really be accessed by the boid calculation class
    """
    my_aboids = new_my_aboids

  def update_all_aboids(self, a_boid_string_list):
    """
    Method to update all a boids, should be a compilation of all a boids from host updates.
	Should receive a list of strings that are the first part of payload from each HUPD
    """
    numpy_array = np.array([])
    for string in a_boid_string_list:
      np.append(numpy_array, self.string_to_numpy_array(string))
    all_aboids = numpy_array

  def create_left_halo(self):
    """
    separate my boids into a left halo, for boids 10 spaces away from xmin
    """
    halo_bounday = x_min+10
    left_halo_array = np.array([])
    for nparray in my_boids: # ask lilly if i can do this
    	if nparray [0] <= halo_boundary:
        np.append(left_halo_array,nparray)
    self.l_halo = left_halo_array

  def ceate_right_halo(self):
    """
    separate my boids into a left halo, for boids 10 spaces away from xmin
    """
    halo_bounday = x_min-10
    right_halo_array = np.array([])
    for nparray in np.nditer(my_boids): # ask lilly if i can do this
    	if nparray[0] >= halo_boundary:
        np.append(right_halo_array,nparray)
    self.r_halo = right_halo_array

  def string_to_numpy_array(self, string):
    numpy_array = np.fromstring(string)
    return numpy_array


  def numpy_array_to_string(self, nparray):
    """
    Method to make np arrays compatible for sending over the wire
    """
    string_form = np.array_str(nparray)
    return string_form
