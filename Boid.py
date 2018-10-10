import time
import numpy as np
#these functions move birds with [x, y] numpy arrays

steps = int(1)
#horizontal/vertical movements
#x coordinate postive shift, no y shift
def move_right(arr):
    arr[0] += steps

#x coordinate negative shift, no y shift
def move_left(arr):
    arr[0] -= steps

#no x shift, y coordinate positive shift
def move_up(arr):
    arr[1] += steps

#no x shift, y coordinate negative shift
def move_down(arr):
    arr[1] -= steps


#diagnoal movements
def move_top_right(arr):
    arr[0] += steps
    arr[1] += steps

def move_top_left(arr):
    arr[0] -= steps
    arr[1] += steps

def move_bot_left(arr):
    arr[0] -= steps
    arr[1] -= steps

def move_bot_right(arr):
    arr[0] += steps
    arr[1] -= steps

#Split the vertical/horizontal movement to its own logic check
def move_xy(boid, a_boid):
    if boid[0] == a_boid[0] and boid[1] < a_boid[1]:
        boid = move_down(boid)
    elif boid[0] == a_boid[0] and boid[1] > a_boid[1]:
        boid = move_up(boid)
    elif boid[1] == a_boid[1] and boid[0] < a_boid[0]:
        boid = move_right(boid)
    elif boid[1] == a_boid[1] and boid[0] > a_boid[0]:
        boid = move_left(boid)

#Split the diag movement to its own logic check
def move_diag(boid, a_boid):
    if boid[1] > a_boid[1] and boid[0] > a_boid[0]:
        boid = move_bot_left(boid)
    elif boid[1] > a_boid[1] and boid[0] < a_boid[0]:
        boid = move_bot_right(boid)
    elif boid[1] < a_boid[1] and boid[0] > a_boid[0]:
        boid = move_top_left(boid)
    elif boid[1] < a_boid[1] and boid[0] < a_boid[0]:
        boid = move_top_right(boid)

#Decide the most efficient move based on coordinates
def decide_move(boid, a_boid):
    if boid[0] == a_boid[0] or boid[1] == a_boid[1]:
        move_xy(boid, a_boid)
    else:
        move_diag(boid, a_boid)

#Loop continually moves boid closer to alpha using vectorized funciton
# def getting_closer(boid, a_boid):
#     while np.array_equal(boid, a_boid) == False:
#         vfunc = np.vectorize(decide_move(boid, a_boid))
#         print(str(boid) + str(a_boid))

def main():
    boid = np.array([7, 2])
    a_boid = np.array([2, 0])
    vfunc = np.vectorize(decide_move(boid, a_boid))

if __name__ == "__main__":
    main()

