'''
COMMUNICATIONS PROTOCOL

sections of each message are seperated by '\n'
information within each section is separated by '\0'

1. connection request = type:CREQ, origin:addr of host sending request, payload:\0
2. okay response = type:OKAY, origin:addr of serverPC, payload:BOID area\0list of host ips separated by \0
3. new host connected (host to serverPC) = type:NHST, origin:addr of new host, payload:list of all dead host ips separated by \0
4. new host connected (host to host) = type:NHST, origin:addr of new host, payload:BOID area
5. host area = type:AREA, origin:addr of host sending, payload:BOID area
6. host update = type:HUPD, origin:addr of host sending, payload:my_boids\0l_halo\0r_halo\0all_l\0all_r\0all_l_alphas\0all_r_alphas\0
7. lost host = type:LHST, origin:addr of host leaving, payload:\0

'''



'''
This message class takes in the type, origin, and payload arguments for the message, and produces a byte string following the provided protocol.
This byte string should be the data that is sent via the connection, and every host receiving the byte string needs to parse it via the protocol.
'''


def parseMessage(sock):
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
        message = self.type + '\n' + self.origin + '\n' + self.payload + '\n';
        return message.encode()
