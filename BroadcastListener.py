import socket
from threading import Thread
import Message
from Message import Message

class BroadcastListener:

    def __init__(self, coord, time_step, socket):
        self.coordinator = coord
        self.socket = socket #not sure if this will work with naming things
        self.last_listened_time_step = time_step #will have to change this
        self.thread = Thread(target=lambda: self.run())
        self.thread.start()


    def handleMessage(self, message):
        if message.type == 'CREQ':
            #only do something if you are the serverPC
        elif message.type == 'NHST':
            #add the new host to list of existing hosts
            #will send the new host's info to the coordinator

        elif message.type == 'HUPD':
            #process the info from the Host Update
            # will send the updated info to the coordinator

        elif message.type == 'CCLS':
            #only do something if you are the serverPC
        elif message.type == 'LHST':
            #remove the lost host from the list of existing hosts
            #will send the lost host's info to the coordinator
            
        else:
            #invalid message type


    def run(self):
        #the main method for the broadcastlistener
        while True:
            #receive an incoming message, if any
            new_message = parseMessage(this.socket)
            #decide what to do with the message


    # a class that is used for threading of the general BroadcastManager
    # each instance of this class and thus thread, is responsible for listening to one socket
    # Should maybe also keep track of the most recent time step calculated, and make sure not to push any info from 2+ timesteps ahead.
    #ask lilly paul or christian tomorrow about how to implement threading in python
