'''
COMMUNICATIONS PROTOCOL

1. New host sends connection request to serverPC
2. serverPC sends out new connection (if accepted) to all existing hosts
3a. a host sends its data per timestep out to every other host (peer to peer)
3b. every host must receive data from every other host at each timestep (peer to peer)
4a. if a host takes too long to send its data for a timestep, it is considered disconnected
4b. a host can send a disconnect message to ther serverPC
5. if a host has been considered disconnected, the serverPC sends a message to all other hosts notifying them of the lost host

information in a message is seperated by '\0'
the end of a message is marked by a '\n'

1. connection request = type:CREQ, origin:addr of host sending request, payload:alias/identifier
2. new host accepted = type:NHST, origin:serverPC addr, payload:new host addr
3. host timestep update = type:HUPD, origin:host sending update, payload:updated BOID info
4. close connection = type:CCLS, origin:addr of host closing connection, payload:none
5. lost host relay = type:LHST, origin:serverPC addr, payload:lost host addr

'''



'''
This message class takes in the type, origin, and payload arguments for the message, and produces a byte string following the provided protocol.
This byte string should be the data that is sent via the connection, and every host receiving the byte string needs to parse it via the protocol.
'''


def parseMessage(sock):
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


class Message:

    def __init__(self, datatype, origin, payload):
        self.type = datatype
        self.origin = origin
        self.payload = payload

    def generateByteMessage(self):
        message = self.type + '\0' + self.origin + '\0' + self.payload + '\n';
        return message
