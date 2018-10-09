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