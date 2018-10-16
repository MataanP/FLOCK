from threading import Thread
from Message import Message
import socket
from HostInfo import HostInfo
import sys

class Host:

    def __init__(self, ip, port, server_ip):
        self.ip = ip #Hosts ip
        self.port = port # Host port
        self.serverPC_ip = server_ip #ServerPC ip the host is connecting to
        self.x_scalar = 50  #for incrementing the x_min to an x_max value
        self.curr_x_max = 0
        self.curr_x_min = 50
        self.curr_x_min_ip = ''
        self.l_neighbor = '' #Area of the shared area between the host and the left neighbor
        self.r_neighbor = '' #Area shared between the host and the right neighbor
        self.host_ips = [] #The list of all connected hosts on the network
        self.connections = [] #A list of connection objects
        self.work_queue = [] #The queue of instructions for the host to execute
        self.all_alphas = [] #List of all host alphas
        self.running = True #Running and updated are semaphores responsible for flagging when the program should execute
        self.updated = False
        self.updates_received = []  # this will be for keeping track of what host we've received an HUPD from
        self.run()

    def parseMessage(self, sock):
        '''ParseMessage is responsible for recieving messages from sockets and and returning them as a string'''
        try:
            msg = b''
            while True:
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed - 1')
                if byte == b'\n':
                    break
                msg += byte
            datatype = msg.decode()
            msg = b''
            while True:
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed - 2')
                if byte == b'\n':
                    break
                msg += byte
            origin = msg.decode()
            msg = b''
            while True:
                byte = sock.recv(1)
                if len(byte) == 0:
                    raise ConnectionError('Socket is closed - 3')
                if byte == b'\n':
                    break
                msg += byte
            payload = msg.decode()
            return Message(datatype, origin, payload)
        except ConnectionError as err:
            print("Error: {0} ".format(err))
            return None

    def parseMessageHost(self, conn):
        '''ParseMessageHost is responsible for recieving messages from host-related sockets and and returning them as a Message object'''
        msg = b''
        while True:
            byte = sock.recv(1)
            if len(byte) == 0:
                print('Host ' + conn.ip + ' was lost')
                range = conn.max_x - conn.min_x
                if self.l_neighbor == conn.ip:
                    self.x_min -= int((range/2.0)+.5)
                    self.host_info.x_min -= int((self.x_scalar/2.0)+.5)
                    self.host_info.merge_left_backups()
                if self.r_neighbor == conn.ip:
                    self.x_max += int((range/2.0)+.5)
                    self.host_info.x_max += int((self.x_scalar/2.0)+.5)
                    self.host_info.merge_right_backups()
                conn.close()
                self.host_ips.remove(conn.ip)
                self.connections.remove(conn)
                return
            if byte == b'\n':
                break
            msg += byte
        datatype = msg.decode()
        msg = b''
        while True:
            byte = sock.recv(1)
            if len(byte) == 0:
                print('Host ' + conn.ip + ' was lost')
                range = conn.max_x - conn.min_x
                if self.l_neighbor == conn.ip:
                    self.x_min -= int((range/2.0)+.5)
                    self.host_info.x_min -= int((self.x_scalar/2.0)+.5)
                    self.host_info.merge_left_backups()
                if self.r_neighbor == conn.ip:
                    self.x_max += int((range/2.0)+.5)
                    self.host_info.x_max += int((self.x_scalar/2.0)+.5)
                    self.host_info.merge_right_backup()
                conn.close()
                self.host_ips.remove(conn.ip)
                self.connections.remove(conn)
                return
            if byte == b'\n':
                break
            msg += byte
        origin = msg.decode()
        msg = b''
        while True:
            byte = sock.recv(1)
            if len(byte) == 0:
                print('Host ' + conn.ip + ' was lost')
                range = conn.max_x - conn.min_x
                if self.l_neighbor == conn.ip:
                    self.x_min -= int((range/2.0)+.5)
                    self.host_info.x_min -= int((self.x_scalar/2.0)+.5)
                    self.host_info.merge_left_backups()
                if self.r_neighbor == conn.ip:
                    self.x_max += int((range/2.0)+.5)
                    self.host_info.x_max += int((self.x_scalar/2.0)+.5)
                    self.host_info.merge_right_backup()
                conn.close()
                self.host_ips.remove(conn.ip)
                self.connections.remove(conn)
                return
            if byte == b'\n':
                break
            msg += byte
        payload = msg.decode()
        return Message(datatype, origin, payload)


    def connectToServer(self):
        """
        This function initiaties the connection request and sends it to the serverPC to be verified as a host.
        The function should then recieve an Okay message, and connect to all hosts sent in the message payload.
        Once the host is connected it will begin the thread listening to the server and work threads
        """
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.bind((self.ip, self.port))
        client_sock.connect((self.serverPC_ip, 9090))
        #create CREQ message
        message = Message('CREQ', self.ip, '\0')
        client_sock.sendall(message.generateByteMessage())
        print('Sent CREQ message to serverPC at ' + self.serverPC_ip)
        #recieve response as string
        response_message = self.parseMessage(client_sock)
        if (response_message.type == 'OKAY'):
            print('OKAY message received')
            #payload contains host area, and list of connected hosts
            payload_array = response_message.payload.split(',')
            i = 1
            lost_payload = ''
            while i < len(payload_array):
                indicator = self.setupHostConnection(payload_array[i])
                if(indicator == False):
                    lost_payload += payload_array[i]+","
                else:
                    self.host_ips.append(payload_array[i])
                i += 1
            self.x_min = self.curr_x_max
            self.x_max = self.x_min + self.x_scalar
            self.host_info = HostInfo(self.x_min, self.x_max)

            if self.curr_x_min_ip == '':
                #there was no other host, you are your own neighbor
                self.r_neighbor = self.ip
                self.host_info.r_neighbor_ip = self.ip
                self.l_neighbor = self.ip
                self.host_info.l_neighbor_ip = self.ip
            else:
                #else, there is another host - check if there are any other hosts
                self.r_neighbor = self.curr_x_min_ip
                self.host_info.r_neighbor_ip = self.curr_x_min_ip

                if self.l_neighbor == '':
                    #there isnt a left neighbor - left neighbor is right neighbor
                    self.l_neighbor = self.r_neighbor
                    self.host_info.l_neighbor_ip = self.r_neighbor
                else:
                    #there is a left neighbor - set host info left neighbor
                    self.host_info.l_neighbor_ip = self.l_neighbor
            #this message contains the hosts that have disconnected from the network and notifes the serverPC about the change
            del_message = Message('LHST', self.ip, lost_payload)
            print('sent LHST to serverPC with payload: ' + lost_payload)
            client_sock.sendall(del_message.generateByteMessage())
            # need to start the listening thread and the work thread now
            listening_thread = Thread(target=lambda: self.listeningPort())
            listening_thread.daemon = True
            listening_thread.start()
            work_thread = Thread(target=lambda: self.processWork())
            work_thread.daemon = True
            work_thread.start()
        else:
            print('Invalid message type received from ' + message.origin)

    def setupHostConnection(self, host_ip):
        """
        This function is responsible for connecting to all hosts on the network.
        The host will also setup it's left and right neighbor and create the listening threads for host connections
        """
        if host_ip != self.ip and host_ip != '':
            host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            indicator = host_socket.connect_ex((host_ip, 9090))
            if indicator != 0:
                return False
            else:
                host_area = self.x_min + ':' + self.x_max
                new_host_msg = Message("NHST", self.ip, host_area)
                host_socket.sendall(new_host_msg.generateByteMessage())
                print('NHST message sent to Host at ' + host_ip)
                area_message = self.parseMessage(client_sock)
                if(area_message.type == 'AREA'):
                    print('AREA message received from ' + area_message.origin)
                    payload_array = area_message.payload.split(':')
                    curr_host_ip = area_message.origin
                    host_min_x = payload_array[0]
                    host_max_x = payload_array[1]
                    if host_max_x > self.curr_x_max:
                        self.curr_x_max = host_max_x
                    if self.min_x == host_max_x:
                        self.l_neighbor = curr_host_ip
                    if host_min_x <= self.curr_x_min:
                        self.curr_x_min = host_min_x
                        self.curr_x_min_ip = curr_host_ip
                    new_thread = Thread(target=lambda: self.listenToHost(host_socket))
                    new_thread.daemon = True
                    new_thread.start()
                    new_connection = Connection(host_ip, host_socket, new_thread, host_min_x, host_max_x)
                    self.connections.append(new_connection)
                    return True
                else:
                    print('Invalid message type received from ' + area_message.origin + ' - Host corrupt')
                    return False
        return True

    def listeningPort(self):
        """
        The listening port uses a binded socket to accept new incoming host connections.
        Once accepted the function will add the NHST instruction to the work queue
        """
        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listening_socket.bind((self.ip, 9090))
        listening_socket.listen(1)
        while self.running == True:
            new_conn_sock, (new_conn_ip, new_conn_port) = listening_socket.accept()
            message = self.parseMessage(new_conn_sock)
            if (message.type == 'NHST'):
                print('Got NHST message from ' + message.origin)
                new_instruction = Instruction('NHST')
                new_instruction.message = message
                new_instruction.sock = new_conn_sock
                self.work_queue.append(new_instruction)
            else:
                print('Invalid Message Type received from ' + message.origin)
                new_conn_sock.close()
        return

    def processWork(self):
        """
        processWork goes through the intruction objects in the work_queue
        processWork prioritizes certain instructions in order to implement implicit
        """
        while self.running == True:
            if len(self.work_queue) == 0:
                self.work_queue = [Instruction('Do Math'), Instruction('Send HUPD'), Instruction('Receive All HUPDs')]
            else:
                instruction = self.work_queue.pop(0)
                if instruction.type == 'Do Math':
                    #start calculations
                    self.updated = False
                    #print('Doing Math')
                    # run calculations
                elif instruction.type == 'Send HUPD':
                    #echo host update to all other hosts on the network
                    all_l, all_r = self.host_info.get_our_backup()
                    all_l_alphas, all_r_alphas = self.host_info.get_our_alpha_backup()
                    min_max = str(self.x_min) + ':' + str(self.x_max)
                    payload = self.host_info.numpy_array_to_string(self.host_info.my_aboids) + '\0' + self.host_info.numpy_array_to_string(self.host_info.l_halo) + '\0' + self.host_info.numpy_array_to_string(self.host_info.r_halo) + '\0' + all_l + '\0' + all_r + '\0' + all_l_alphas + '\0' + all_r_alphas + '\0' + min_max + '\0'
                    our_update = Message("HUPD", self.ip, payload)

                    #if there are no connections, send to myself
                    if len(self.connections) == 0:
                        self.updateSelf(our_update)
                    else:
                        for connection in self.connections:
                            connection.sock.sendall(our_update.generateByteMessage())
                    self.host_info.update_my_aboids()
                    print('Sent Out HUPD')
                elif instruction.type == 'Receive All HUPDs':
                    # make sure to receive all HUPDs from listening threads
                    if len(self.connections) > 0:
                        while len(self.updates_received) != len(self.connections):
                            msg = 'wait'
                    # only set to true once all updates have been received
                    self.updated = True
                    self.updates_received = []
                    # Once all updates are recieved update ABoid locations
                    self.host_info.merge_halos()
                    self.host_info.update_all_aboids(self.all_alphas)
                    self.all_alphas = []
                elif instruction.type == 'NHST':
                    #New host tring to connect to network
                    new_host_ip = instruction.message.origin
                    payload_array = instruction.message.payload.split(':')
                    new_host_min_x = payload_array[0]
                    new_host_max_x = payload_array[1]
                    #check if the new host is a neighbor
                    if self.x_max == new_host_min_x:
                        self.r_neighbor = new_host_ip
                        self.host_info.r_neighbor_ip = new_host_ip
                    if self.x_min == 0:
                        self.l_neighbor = new_host_ip
                        self.host_info.l_neighbor_ip = new_host_ip
                    self.host_ips.append(new_host_ip)
                    #Start the thread that is listening to the socket connected to the new host
                    new_thread = Thread(target=lambda: self.listenToHost(instruction.sock))
                    new_thread.daemon = True
                    new_thread.start()
                    new_connection = Connection(new_host_ip, instruction.sock, new_thread, new_host_min_x, new_host_max_x)
                    self.connections.append(new_connection)
                    host_area = self.x_min + ':' + self.x_max
                    #send current host area to the newly connected host
                    area_message = Message('AREA', self.ip, host_area)
                    instruction.sock.sendall(area_message.generateByteMessage())
                    print('Sent AREA message to ' + new_host_ip)
                elif instruction.type == 'LHST':
                    #Host has disconnected to the network
                    for host_ip in self.host_ips:
                        if host_ip == instruction.message.origin:
                            #remove host from list of connected ips
                            self.host_ips.remove(host_ip)
                    for connection in self.connections:
                        #remove the connection object from list of known connections
                        if connection.ip == instruction.message.origin:
                            #close the hosts socket and thread
                            connection.close()
                            self.connections.remove(connection)
                else:
                    print('Invalid Instruction - skipping...')

        return

    def updateSelf(self, message):
        self.updated = False
        host_ip = message.origin
        payload = message.payload.split('\0')
        host_alphas = payload[0]
        host_l_halo = payload[1]
        host_r_halo = payload[2]
        host_all_l = payload[3]
        host_all_r = payload[4]
        l_alpha_backup = payload[5]
        r_alpha_backup = payload[6]
        host_min = payload[7].split(':')[0]
        host_max = payload[7].split(':')[1]
        if self.l_neighbor == host_ip:
            #if the hosts left neighbor then store the halo region data and create back ups of left neighbor data
            self.host_info.n_l_halo = self.host_info.string_to_numpy_array(host_r_halo)
            self.host_info.l_backup = host_all_r
            self.host_info.l_backup_alphas = r_alpha_backup
        if self.r_neighbor == host_ip:
            #if the hosts right neighbor then store the halo region data and create back ups of right neighbor data
            self.host_info.n_r_halo = self.host_info.string_to_numpy_array(host_l_halo)
            self.host_info.r_backup = host_all_l
            self.host_info.r_backup_alphas = l_alpha_backup
        self.updated = True

    def listenToHost(self, host_sock):
        """
        listenToHost recieves messages from other hosts
        If a host update is received the host will check if it is a neighbor, and then update the neighbor halo region and backups
        If a lost host message is recieved it will create the instruction type LHST and added to the queue
        """
        while self.running == True:
            #turn message into string
            host_connection = None
            for conn in self.connections:
                if conn.sock == host_sock:
                    host_connection = conn
            message = self.parseMessageHost(host_connection)
            if message.type == 'HUPD':
                #host update message payload
                print('Got HUPD from ' + message.origin)
                self.updated = False
                host_ip = message.origin
                payload = message.payload.split('\0')
                host_alphas = payload[0]
                host_l_halo = payload[1]
                host_r_halo = payload[2]
                host_all_l = payload[3]
                host_all_r = payload[4]
                l_alpha_backup = payload[5]
                r_alpha_backup = payload[6]
                host_min = payload[7].split(':')[0]
                host_max = payload[7].split(':')[1]
                if self.l_neighbor == host_ip:
                    #if the hosts left neighbor then store the halo region data and create back ups of left neighbor data
                    self.host_info.n_l_halo = self.host_info.string_to_numpy_array(host_r_halo)
                    self.host_info.l_backup = host_all_r
                    self.host_info.l_backup_alphas = r_alpha_backup

                if self.r_neighbor == host_ip:
                    #if the hosts right neighbor then store the halo region data and create back ups of right neighbor data
                    self.host_info.n_r_halo = self.host_info.string_to_numpy_array(host_l_halo)
                    self.host_info.r_backup = host_all_l
                    self.host_info.r_backup_alphas = l_alpha_backup
                #may need to parse the different Alpha coordinates before appending to all_alphas
                self.all_alphas.append(host_alphas)
                self.updates_received.append(host_ip)
                while (self.updated != True):
                    wait = 'wait'
            elif message.type == 'LHST':
                #LHST message recieved meaning that the host must close that connected socket
                print('Got LHST from ' + message.origin)
                new_instruction = Instruction('LHST')
                new_instruction.message = message
                self.work_queue.append(new_instruction)
            else:
                print('Invalid message type received from ' + message.origin)
        return

    def run(self):
        main_thread = Thread(target=lambda: self.connectToServer())
        main_thread.daemon = True
        main_thread.start()
        while (self.running == True):
            user_input = input('Enter "quit" to end program: ')
            if user_input == 'quit':
                print('Quitting...')
                self.running = False

class Connection:
    def __init__(self, ip, sock, thread,new_min,new_max):
        """
        Connection objects are made up of host ip, sockets and threads so they can be differentiated
        """
        self.ip = ip
        self.host_sock = sock
        self.host_thread = thread
        self.x_min = new_min
        self.x_max = new_max

    def close(self):
        # connection close function for closing sockets and threads
        self.host_sock.close()
        self.host_thread.exit()
        print("Host has been disconnected")


class Instruction:
    """
    Instruction objects are used to specify the instruction type, message and specific host socket
    """
    def __init__(self, type):
        self.type = type
        self.message = None
        self.sock = None

def main():
    if len(sys.argv)<4:
        print("Usage: <YourIP> <YourPort> <ServerIP>")
    else:
        Host(sys.argv[1],int(sys.argv[2]),sys.argv[3])

if __name__ == '__main__':
    main()
