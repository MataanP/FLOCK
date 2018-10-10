'''
COMMUNICATIONS PROTOCOL

1a. New host sends CREQ to serverPC
1b. serverPC sends NHST message to all existing hosts
1c. all hosts receive NHST, attempt to connect to new host
1d. once connected to new host, existing host sends ACKN back to serverPC
1e. if existing host can't connect to new host, existing host is unresponsive + should be disconnected
1f. once all existing hosts have responded to serverPC with ACKN, serverPC sends OKAY to new host
2a. serverPC sends STEP message to all hosts, starting new timestep
2b. all hosts receive STEP message, run their timestep calculations, and broadcast their HUPD to all other hosts
2c. when a host has received a HUPD from all other hosts, the host sends serverPC a SYNC message
2d. when serverPC has received SYNC from all hosts, it is safe to proceed to next timestep
2e. if a host doesn't send SYNC, it is unresponsive + should be disconnected
3a. Existing host sends serverPC a CCLS messag to disconnect from network
3b. serverPC sends all other hosts a LHST message
3c. all hosts receive LHST message, close connection to lost host + forget about lost host, reply to serverPC with ACKN
3d. once serverPC receives ACKN from all other hosts, it is safe to proceed to next timestep
4a. Existing host doesn't reply to serverPC/is unresponsive: serverPC jumps to step 3b, with unresponsize host as lost host

information in a message is seperated by '\0'
the end of a message is marked by a '\n'

1. connection request = type:CREQ, origin:addr of host sending request, payload:alias/identifier
2. new host accepted = type:NHST, origin:serverPC addr, payload:new host addr
3. acknowledgement to serverPC = type:ACKN, origin:addr of host responding, payload:?
4. connection accepted = type:OKAY, origin:serverPC addr, payload:new host addr
5. begin new timestep = type:STEP, origin:serverPC addr, payload:?
6. host timestep update = type:HUPD, origin:addr of host sending update, payload: update info
7. host fully synched = type:SYNC, origin:addr of host updated, payload:?
8. close connection = type:CCLS, origin:addr of host closing connection, payload:none
9. lost host relay = type:LHST, origin:serverPC addr, payload:lost host addr

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
        return message.encode()
