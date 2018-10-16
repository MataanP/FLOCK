# This file makes a boid that follows an alpha boid. The alpha boid moves randomly so they eventually are in sync.
# The next step is to have the alpha bird move away from the regular boid.
import random

boid = [0, 0]
a_boid = [5, 12]

def a_boid_moves(bird):
#make some a_boid movements
    step = random.randint(1, 4)
    if step == 1:
        a_boid[0] += 1
    elif step == 2:
        a_boid[0] -= 1
    elif step == 3:
        a_boid[1] += 1
    elif step == 4:
        a_boid[1] -= 1
    return a_boid

#boid moves along x axis and then y
def boid_moves(bird):
    if boid[0] < a_boid[0]:
        boid[0] += 1
    elif boid[0] > a_boid[0]:
        boid[0] -= 1
    elif boid[1] > a_boid[1]:
        boid[1] -= 1
    elif boid[1] < a_boid[1]:
        boid[1] += 1
    return boid

for i in range(100):
    print(a_boid_moves(a_boid),(boid_moves(boid)))