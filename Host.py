from threading import Thread
from Message import Message
import socket
import HostInfo

class Host:

    def __init__(self, ip, port, server_ip):
        self.ip = ip
        self.port = port
        self.serverPC_ip = server_ip
        self.x_min = ''
        self.x_max = ''
        self.l_neighbor = ''
        self.r_neightbor = ''
        self.host_ips = []
        self.connections = []
        self.work_queue = []
        self.all_alphas = []
        # to 'pop' off the first thing in queue, use workQueue.pop(0) to pop off + return thing at index 0
        # to add things to the workQueue, use workQueue.append(thing)
        self.host_info = HostInfo(x_min, x_max)
        self.running = True
        self.updated = False
        self.updates_received = []  # this will be for keeping track of what host we've received an HUPD from
        self.run()

    def parseMessage(self, sock):
        try:
            # parse the type
            msg = b''
            while True:
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed - 1')
                if byte == b'\n':
                    break
                msg += byte
            datatype = msg.decode()
            # parse the origin address
            msg = b''
            while True:
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed - 2')
                if byte == b'\n':
                    break
                msg += byte
            origin = msg.decode()
            # parse the payload
            msg = b''
            while True:
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed - 3')
                if byte == b'\n':
                    break
                msg += byte
            payload = msg.decode()
            # create the message
            return Message(datatype, origin, payload)
        except ConnectionError as err:
            print("Error: {0} ".format(err))
            # Error reading from socket
            print('uh oh - message not received')
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
            lost_payload = ''
            while i < len(payload_array):
                #call to setupHostConnections()
                #if above returns false or whatever then dont add, then tell serverPC_ip
                # otherwise append
                indicator = self.setupHostConnection(payload_array[i])
                if(indicator == False):
                    #dont add to list of ips and tell serverPC to remove from its list of ips
                    lost_payload += payload_array[i]+","
                else:
                    self.host_ips.append(payload_array[i])
                i += 1
            del_message = Message('LHST', self.ip, lost_payload)
            print('sent LHST to serverPC with payload: ' + lost_payload)
            client_sock.sendall(del_message.generateByteMessage())

            # ready to call new function
            # here, all of the host connections have been set up
            # need to start the listening thread and the work thread now
            listening_thread = Thread(target=lambda: self.listeningPort())
            listening_thread.daemon = True
            listening_thread.start()

            #need to pass neighbor updates somewhere / use them somewhere
            #create host info object

            work_thread = Thread(target=lambda: self.processWork())
            work_thread.daemon = True
            work_thread.start()
        else:
            # invalid message type - can not connect to network
            print('Invalid message type received')

    def setupHostConnection(self, host_ip):
        if host_ip != self.ip and host_ip != '':
            host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            indicator = host_socket.connect_ex((host_ip, 9090))
            if indicator != 0:
                return False
            else:
                #need to replace self.host_area with the self.min_x:self.max_x once we implement
                host_area = self.x_min + ':' + self.x_max
                new_host_msg = Message("NHST", self.ip, host_area)
                host_socket.sendall(new_host_msg.generateByteMessage())
                #receive new AREA Message - this tells us this hosts' min_x and max_x for determining if they are this host's neighbor
                area_message = self.parseMessage(client_sock)
                if(area_message.type == 'AREA'):
                    #correct message received
                    print('AREA message received')
                    payload_array = area_message.payload.split(':')
                    curr_host_ip = area_message.origin
                    host_min_x = payload_array[0]
                    host_max_x = payload_array[1]
                    if self.min_x == host_max_x:
                        #this means the host is this host's l_neighbor
                        self.l_neighbor = curr_host_ip
                    elif host_min_x == 0:
                        #this means the host is this new host's r_neighbor
                        self.r_neightbor = curr_host_ip
                else:
                    # invalid message type - can not connect to network
                    print('Invalid message type received')


                new_thread = Thread(target=lambda: self.listenToHost(host_socket))
                new_thread.daemon = True
                new_thread.start()
                self.connections.append(Connection(host_ip, host_socket, new_thread))
        return True

    def listeningPort(self):
        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listening_socket.bind((self.ip, 9090))
        listening_socket.listen(1)
        while self.running == True:
            new_conn_sock, (new_conn_ip, new_conn_port) = listening_socket.accept()
            message = self.parseMessage(new_conn_sock)
            if (message.type == 'NHST'):
                print('Got NHST message!')
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
                    #print('Doing Math')
                    # run calculations
                elif instruction.type == 'Send HUPD':
                    # broadcast out this host's HUPD
                    msg = 'msg'
                    all_l, all_r = self.host_info.get_our_backup()
                    all_l_alphas, all_r_alphas = self.host_info.get_our_alpha_backup()
                    #Missing functions to make payload in info host
                    payload = self.host_info.my_aboids + '\0' + self.host_info.l_halo + '\0' + self.host_info.r_halo + '\0' + all_l + '\0' + all_r + '\0' + all_l_alphas + '\0' + all_r_alphas + '\0'
                    our_update = Message("HUPD", self.ip, payload)
                    for connection in self.connections:
                        connection.sock.sendall(our_update.generateByteMessage())
                    #print('Broadcasting Out HUPD')
                elif instruction.type == 'Receive All HUPDs':
                    # make sure to receive all HUPDs from listening threads
                    msg = 'msg'
                    while len(self.updates_received) != len(self.connections):
                        msg = 'wait'
                    #print('Receiving all HUPDs')
                    # only set to true once all updates have been received
                    self.updated = True
                    self.updates_received = []
                    #make sure to hand self.all_alphas to self.host_info before resetting
                    self.all_alphas = []
                elif instruction.type == 'NHST':
                    # run a function to add the new host ip to the list of host ip + add new host connection to the list of connections

                    #respond to the new host with an AREA Message
                    host_area = self.x_min + ':' + self.x_max
                    area_message = Message('AREA', self.ip, host_area)
                    #send the AREA message on the socket
                    instruction.sock.sendall(area_message.generateByteMessage())

                    new_host_ip = instruction.message.origin
                    payload_array = instruction.message.payload.split(':')
                    new_host_min_x = payload_array[0]
                    new_host_max_x = payload_array[1]
                    #once we have HostInfo implemented, need to pass this info somewhere to check if new host is a neighbor
                    #waiting for host_info class stuff
                    self.host_ips.append(new_host_ip)
                    new_thread = Thread(target=lambda: self.listenToHost(instruction.sock))
                    new_thread.daemon = True
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
                host_ip = message.origin
                payload = message.payload.split('\0')
                host_alphas = payload[0]
                host_l_halo = payload[1]
                host_r_halo = payload[2]
                host_all_l = payload[3]
                host_all_r = payload[4]
                l_alpha_backup = payload[5]
                r_alpha_backup = payload[6]
                # pass message payload somewhere so they can be used for next calculcations
                if self.l_neighbor == host_ip:
                    self.host_info.n_l_halo = host_r_halo
                    self.host_info.l_backup = host_all_r
                    self.host_info.l_backup_alphas = r_alpha_backup
                elif self.r_neightbor == host_ip:
                    self.host_info.n_r_halo = host_l_halo
                    self.host_info.r_backup = host_all_l
                    self.host_info.r_backup_alphas = l_alpha_backup
                self.all_alphas.append(host_alphas)
                self.updates_received.append(host_ip)
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
        main_thread.daemon = True
        main_thread.start()
        while (self.running == True):
            user_input = input('Enter "quit" to end program: ')
            if user_input == 'quit':
                main_thread.join()
                print('Quitting...')
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

Host('172.16.143.24', 9000, '172.16.135.204')
