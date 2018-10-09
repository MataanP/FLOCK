import math
import random
from itertools import combinations
import time
import numpy as np
from scipy.spatial.distance import pdist

random.seed(a = 42)
list_birds = []

for i in range(1000):
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    bird = (x, y)
    list_birds.append(bird)


def distance(a, b):
    x = (a[0] - b[0]) ** 2
    y = (a[1] - b[1]) ** 2

    dist = math.sqrt(x + y)
    return dist

start = time.time()
for combo in combinations(list_birds, 2):
    distance(combo[0], combo[1])
end = time.time()
print(end - start)
#.00075793 for 9 birds where distance is calculated 9! with PRINTING
#6.584 for 1000 birds where disance is calculated factorially with PRINTING
#.8400 for 1000 birds where distance is NOT calculated without printing
#.875 for 1000 birds where distance is calculated without printing

array_birds = np.random.rand(1000, 2)
start = time.time()
pdist(array_birds)
end = time.time()
print(end - start)
print(pdist(array_birds).shape)

#0.004661083221435547 for 1000 birds distance calculation