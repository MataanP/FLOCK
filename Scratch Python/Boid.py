import numpy as np

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

