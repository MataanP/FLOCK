import numpy as np
import directions
from scipy.ndimage import measurements

#Split the vertical/horizontal movement to its own logic check
def a_move_xy(boid, a_boid):
    if boid[0] == a_boid[0] and boid[1] < a_boid[1]:
        a_boid = move_down(a_boid)
    elif boid[0] == a_boid[0] and boid[1] > a_boid[1]:
        a_boid = move_up(a_boid)
    elif boid[1] == a_boid[1] and boid[0] < a_boid[0]:
        a_boid = move_right(a_boid)
    elif boid[1] == a_boid[1] and boid[0] > a_boid[0]:
        a_boid = move_left(a_boid)

#Split the diag movement to its own logic check
def a_move_diag(boid, a_boid):
    if boid[1] > a_boid[1] and boid[0] > a_boid[0]:
        a_boid = move_bot_left(a_boid)
    elif boid[1] > a_boid[1] and boid[0] < a_boid[0]:
        a_boid = move_bot_right(a_boid)
    elif boid[1] < a_boid[1] and boid[0] > a_boid[0]:
        a_boid = move_top_left(a_boid)
    elif boid[1] < a_boid[1] and boid[0] < a_boid[0]:
        a_boid = move_top_right(a_boid)

#Decide the most efficient move based on coordinates
def a_decide_move(boid, a_boid):
    if boid[0] == a_boid[0] or boid[1] == a_boid[1]:
        a_move_xy(boid, a_boid)
    else:
        a_move_diag(boid, a_boid)

def main():
    a_boid = np.array([2, 0])
    boid_arr = np.random.randint(-50, 50, size=(4, 2))
    centroid = np.rint(measurements.center_of_mass(boid_arr))
    print(centroid)
    vfunc = np.vectorize(a_decide_move(centroid, a_boid))
    print(a_boid)

if __name__ == "__main__":
    main()



