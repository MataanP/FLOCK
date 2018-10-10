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
        if message.type == 'CREQ':
            #CREQ only gets sent from new host to serverPC
            #only serverPC reacts, otherwise incorrect message
            #serverPC reacts by sending NHST message to all exisitng hosts

            #check if this serverPC. if not, the message was sent incorrectly; else, process request as serverPC
            #if serverPC, hand message to serverPC method for adding a new host to the network
            #THIS IS NOT SERVERPC
            print('CREQ received - bad')

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

        elif message.type == 'ACKN':
            #ACKN only gets sent to the serverPC from existing hosts
            #sent either when existing host has connected to new host, or existing host has disconnected from lost host
            #serverPC must wait for an ACKN from all active hosts

            #check if this is serverPC. if not, message sent incorrectly
            #if serverPC, make note that host sent acknowledgement
            print('ACKN received - bad')

        elif message.type == 'OKAY':
            #OKAY only gets sent from serverPC to new host when successfully connected
            #new host is now a host, and can act as such

            #check if this is a new host waiting to be accepted. if not, message sent incorrectly
            #if new host, now accepted into the system
            print('OKAY received - good')

        elif message.type == 'STEP':
            #STEP sent out from serverPC to all hosts, indicating new timestep
            #when hosts receive STEP, they can perform new timestep calculations + broadcast out their HUPD to all other hosts

            #check if this is a host. if not, message sent incorrectly
            #if a host, run new timestep BOID calculations + broadcast out HUPD
            print('STEP received - good')

        elif message.type == 'HUPD':
            #HUPD sent out from every host to every other host
            #when host receives another host's HUPD, must mark that it was received + process payload data
            #all hosts must receive an HUPD from every other host before sending SYNC to serverPC

            #check if this is a host. if not, message sent incorrectly
            #if a host, make note of the host you got an update from + process update info
            print('HUPD received - good')

        elif message.type == 'SYNC':
            #SYNC only sent from fully-updated host to serverPC
            #serverPC must receive a SYNC from all active hosts before allowing new timestep to begin
            #if a host doesn't send a SYNC within a timeframe, it is considered disconnected

            #check if this is serverPC. if not, message sent incorrectly
            #if serverPC, make note that specific host is synchronized
            print('SYNC received - bad')

        elif message.type == 'CCLS':
            #CCLS only sent from existing host to serverPC, telling serverPC that the host is leaving the network
            #when serverPC receives CCLS, must send out LHST to all other hosts so that they can disconnect from lost host

            #check if this is serverPC. if not, message sent incorrectly; else, remove host from list + sent LHST to all existing hosts
            #if serverPC, hand message to serverPC method for removing an existing host from network
            print('CCLS received - bad')

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
