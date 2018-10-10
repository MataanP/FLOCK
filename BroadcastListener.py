import socket
from threading import Thread
import Message
from Message import Message

class BroadcastListener:

    def __init__(self, coord, time_step, socket):
        self.coordinator = coord    #the coordinator for this broadcast listener
        self.socket = socket        #not sure if this will work with naming things
        self.last_listened_time_step = time_step #will have to change this
        self.thread = Thread(target=lambda: self.run())
        self.thread.start()

        #the broadcast listener will need to be given a ROLE (such as host or serverPC) so that it knows how to handle different messages


    def handleMessage(self, message):
        if message.type == 'CREQ':
            #CREQ only gets sent from new host to serverPC
            #only serverPC reacts, otherwise incorrect message
            #serverPC reacts by sending NHST message to all exisitng hosts
            print('CREQ received')

        elif message.type == 'NHST':
            #NHST only sent from serverPC to existing hosts
            #hosts connect to the new host, add new host to list of hosts, and reply to serverPC with ACKN once connected
            #new host info will be passed to coordinator
            print('NHST received')

        elif message.type == 'ACKN':
            #ACKN only gets sent to the serverPC from existing hosts
            #sent either when existing host has connected to new host, or existing host has disconnected from lost host
            #serverPC must wait for an ACKN from all active hosts
            print('ACKN received')

        elif message.type == 'OKAY':
            #OKAY only gets sent from serverPC to new host when successfully connected
            #new host is now a host, and can act as such
            print('OKAY received')

        elif message.type == 'STEP':
            #STEP sent out from serverPC to all hosts, indicating new timestep
            #when hosts receive STEP, they can perform new timestep calculations + broadcast out their HUPD to all other hosts
            print('STEP received')

        elif message.type == 'HUPD':
            #HUPD sent out from every host to every other host
            #when host receives another host's HUPD, must mark that it was received + process payload data
            #all hosts must receive an HUPD from every other host before sending SYNC to serverPC
            print('HUPD received')

        elif message.type == 'SYNC':
            #SYNC only sent from fully-updated host to serverPC
            #serverPC must receive a SYNC from all active hosts before allowing new timestep to begin
            #if a host doesn't send a SYNC within a timeframe, it is considered disconnected
            print('SYNC received')

        elif message.type == 'CCLS':
            #CCLS only sent from existing host to serverPC, telling serverPC that the host is leaving the network
            #when serverPC receives CCLS, must send out LHST to all other hosts so that they can disconnect from lost host
            print('CCLS received')

        elif message.type == 'LHST':
            #LHST only sent from serverPC to existing hosts
            #when existing host receives LHST, must close socket shared w/ lost host and remove the lost host from list of known hosts
            #once lost host has been successfully disconnected/forgotten by existing host, existing host replies to serverPC with ACKN
            #all existing hosts must send an ACKN response to the serverPC after receiving LHST; else, they are considered disconnected
            print('LHST received')

        else:
            #invalid message type
            print('Invalid message type received')


    def parseMessage(self, sock):
        try:
            #parse the type
            while True:
                msg = b''
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed')
                if byte == b'\0':
                    break
                msg += byte
            datatype = msg.decode()
            #parse the origin address
            while True:
                msg = b''
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed')
                if byte == b'\0':
                    break
                msg += byte
            origin = msg.decode()
            #parse the payload
            while True:
                msg = b''
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed')
                if byte == b'\n':
                    break
                msg += byte
            payload = msg.decode()
            #create the message
            return Message(datatype, origin, payload)
        except:
            #Error reading from socket
            return None


    def run(self):
        #the main method for the broadcastlistener
        while True:
            #receive an incoming message, if any
            new_message = self.parseMessage(self.socket)
            self.handleMessage(new_message)
            #decide what to do with the message


    # a class that is used for threading of the general BroadcastManager
    # each instance of this class and thus thread, is responsible for listening to one socket
    # Should maybe also keep track of the most recent time step calculated, and make sure not to push any info from 2+ timesteps ahead.
    #ask lilly paul or christian tomorrow about how to implement threading in python
