import socket
def Class BroadcastListener:

    def __init__(self, time_step, socket):
        self.socket = socket #not sure if this will work with naming things
        self.last_listened_time_step = time_step #will have to change this

    # a class that is used for threading of the general BroadcastManager
    # each instance of this class and thus thread, is responsible for listening to one socket
    # Should maybe also keep track of the most recent time step calculated, and make sure not to push any info from 2+ timesteps ahead.
    #ask lilly paul or christian tomorrow about how to implement threading in python
