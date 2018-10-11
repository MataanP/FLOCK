from threading import Thread
from Message import Message
import socket


class Host:

    def __init__(self, ip, port, server_ip):
        self.ip = ip
        self.port = port
        self.serverPC_ip = server_ip
        self.host_area = 'boid area'
        self.host_ips = []
        self.connections = []
        self.work_queue = []
        # to 'pop' off the first thing in queue, use workQueue.pop(0) to pop off + return thing at index 0
        # to add things to the workQueue, use workQueue.append(thing)
        self.running = True
        self.updated = False
        self.updates_received = []  # this will be for keeping track of what host we've received an HUPD from
        self.connectToServer()

    def parseMessage(self, sock):
        try:
            # parse the type
            msg = b''
            while True:
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed')
                if byte == b'\n':
                    break
                msg += byte
            datatype = msg.decode()
            # parse the origin address
            msg = b''
            while True:
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed')
                if byte == b'\n':
                    break
                msg += byte
            origin = msg.decode()
            # parse the payload
            msg = b''
            while True:
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed')
                if byte == b'\n':
                    break
                msg += byte
            payload = msg.decode()
            # create the message
            return Message(datatype, origin, payload)
        except:
            # Error reading from socket
            return None

    def connectToServer(self):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.bind((self.ip, self.port))
        client_sock.connect((self.serverPC_ip, 9090))
        message = Message('CREQ', self.ip, '\0')
        client_sock.sendall(message.generateByteMessage())
        response_message = self.parseMessage(client_sock)
        if (response_message.type == 'OKAY'):
            print('OKAY message received')
            payload_array = response_message.payload.split(',')
            self.host_area = payload_array[0]
            i = 1
            while i < len(payload_array):
                self.host_ips.append(payload_array[i])
                i += 1
            # ready to call new function
            self.setupHostConnections()
        else:
            # invalid message type - can not connect to network
            print('Invalid message type received')

    def setupHostConnections(self):
        for host_ip in self.host_ips:
            host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host_socket.connect((host_ip, 9090))
            new_host_msg = Message("NHST", self.ip, self.host_area)
            host_socket.sendall(new_host_msg.generateByteMessage())
            new_thread = Thread(target=lambda: self.listenToHost(host_socket))
            new_thread.start()
            self.connections.append(Connection(host_ip, host_socket, new_thread))
        # here, all of the host connections have been set up
        # need to start the listening thread and the work thread now
        listening_thread = Thread(target=lambda: self.listeningPort())
        listening_thread.start()
        work_thread = Thread(target=lambda: self.processWork())
        work_thread.start()

    def listeningPort(self):
        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listening_socket.bind((self.ip, 9090))
        listening_socket.listen(1)
        while self.running == True:
            new_conn_sock, (new_conn_ip, new_conn_port) = listening_socket.accept()
            message = self.parseMessage(new_conn_sock)
            if (message.type == 'NHST'):
                new_instruction = Instruction('NHST')
                new_instruction.message = message
                new_instruction.sock = new_conn_sock
                self.work_queue.append(new_instruction)
            else:
                print('Invalid Message Type received')
        return

    def processWork(self):
        while self.running == True:
            if len(self.work_queue) == 0:
                self.work_queue = [Instruction('Do Math'), Instruction('Send HUPD'), Instruction('Receive All HUPDs')]
            else:
                instruction = self.work_queue.pop(0)
                if instruction.type == 'Do Math':
                    self.updated = False
                    print('Doing Math')
                # run calculations
                elif instruction.type == 'Send HUPD':
                    # broadcast out this host's HUPD

                    print('Broadcasting Out HUPD')
                elif instruction.type == 'Receive All HUPDs':
                    # make sure to receive all HUPDs from listening threads

                    print('Receiving all HUPDs')
                    # only set to true once all updates have been received
                    self.updated = True
                elif instruction.type == 'NHST':
                    # run a function to add the new host ip to the list of host ip + add new host connection to the list of connections
                    new_host_ip = instruction.message.origin
                    self.host_ips.append(new_host_ip)
                    new_thread = Thread(target=lambda: self.listenToHost(instruction.sock))
                    new_thread.start()
                    self.connections.append(Connection(new_host_ip, instruction.sock, new_thread))

                elif instruction.type == 'LHST':
                    for host_ip in self.host_ips:
                        if host_ip == instruction.message.origin:
                            self.host_ips.remove(host_ip)
                    # here, host_ip was removed from list of host_ips
                    for connection in self.connections:
                        if connection.ip == instruction.message.origin:
                            connection.close()
                            self.connections.remove(connection)
                # here, the connection for the host was closed + connection was removed from list of connections

                else:
                    print('Invalid Instruction - skipping...')

        return

    def listenToHost(self, host_sock):
        while self.running == True:
            message = self.parseMessage(host_sock)
            if message.type == 'HUPD':
                # pass message payload somewhere so they can be used for next calculcations
                self.updates_received.append(message.origin)

                while (self.updated != True):
                    # wait
                    wait = 'wait'
            elif message.type == 'LHST':
                new_instruction = Instruction('LHST')
                new_instruction.message = message
                self.work_queue.append(new_instruction)
            else:
                print('Invalid message type received')
        return

    def run(self):
        main_thread = Thread(target=lambda: self.connectToServer())
        main_thread.start()
        while (self.running == True):
            user_input = input('Enter "quit" to end program: ')
            if user_input == 'quit':
                self.running = False


class Connection:
    def __init__(self, ip, sock, thread):
        self.ip = ip
        self.host_sock = sock
        self.host_thread = thread

    def close(self):
        # connection close function for closing sockets and threads
        self.host_sock.close()
        self.host_thread.exit()
        print("Host has been disconnected")


class Instruction:
    def __init__(self, type):
        self.type = type
        self.message = None
        self.sock = None
