import socket
from threading import Thread
import Message
from Message import Message

class BroadcastListener:

    def __init__(self, connection_manager, socket):
        self.conn_man = connection_manager    #the coordinator for this broadcast listener
        self.socket = socket        #not sure if this will work with naming things
        self.thread = Thread(target=lambda: self.run())
        self.thread.start()

        #the broadcast listener will need to be given a ROLE (such as host or serverPC) so that it knows how to handle different messages


    def handleMessage(self, message):
        elif message.type == 'NHST':
            #NHST only sent from serverPC to existing hosts
            #hosts connect to the new host, add new host to list of hosts, and reply to serverPC with ACKN once connected
            #new host info will be passed to coordinator

            #check if this is a host. if not, message sent incorrectly
            #if a host, try to connect to the new host; if successful, send ACKN back to serverPC

            print('NHST received - good')
            payload_array = message.payload.split(':')
            if len(payload_array) == 2:
                ip = payload_array[0]
                port = int(payload_array[1])
                self.conn_man.add_host_with_address(ip, port)
            #else:
                #ERROR

        
        elif message.type == 'LHST':
            #LHST only sent from serverPC to existing hosts
            #when existing host receives LHST, must close socket shared w/ lost host and remove the lost host from list of known hosts
            #once lost host has been successfully disconnected/forgotten by existing host, existing host replies to serverPC with ACKN
            #all existing hosts must send an ACKN response to the serverPC after receiving LHST; else, they are considered disconnected

            #check if this is a host. if not, message sent incorrectly
            #if a host, close socket shared w/ lost host and remove lost host from list of hosts, then reply to serverPC with ACKN
            print('LHST received - good')
            payload_array = message.payload.split(':')
            ip = payload_array[0]
            self.conn_man.remove_host(ip)

        elif message.type == 'HUPD':
            #HUPD sent out from every host to every other host
            #when host receives another host's HUPD, must mark that it was received + process payload data
            #all hosts must receive an HUPD from every other host before sending SYNC to serverPC

            #check if this is a host. if not, message sent incorrectly
            #if a host, make note of the host you got an update from + process update info
            print('HUPD received - good')


        else:
            #invalid message type
            print('Invalid message type received')


    def parseMessage(self, sock):
        try:
            #parse the type
            msg = b''
            while True:
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed')
                if byte == b'\n':
                    break
                msg += byte
            datatype = msg.decode()
            print('type is ' + datatype)
            #parse the origin address
            msg = b''
            while True:
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed')
                if byte == b'\n':
                    break
                msg += byte
            origin = msg.decode()
            print('origin is ' + origin)
            #parse the payload
            msg = b''
            while True:
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed')
                if byte == b'\n':
                    break
                msg += byte
            payload = msg.decode()
            print('payload is ' + payload)
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
