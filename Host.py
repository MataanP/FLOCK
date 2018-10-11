import Message
import threading


class Host:

    def __init__(self, ip, port, server_ip):
        self.ip = ip
        self.port = port
        self.serverPC_ip = server_ip
        self.host_area = 'boid area'
        self.host_ips = []
        self.connections = []
        self.workQueue = []
        #to 'pop' off the first thing in queue, use workQueue.pop(0) to pop off + return thing at index 0
        #to add things to the workQueue, use workQueue.append(thing)
        self.running = True
        self.updated = False
        self.updates_received = []  #this will be for keeping track of what host we've received an HUPD from

    def connectToServer(self):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.bind((self.ip, self.port))
        client_sock.connect((self.serverPC_ip, 9090))
        message = Message('CREQ', self.ip, '\0')
        client_sock.sendall(message.generateByteMessage())
        response_message = self.parseMessage(client_sock)
        if(response_message.type == 'OKAY'):
            print('OKAY message received')
            payload_array = response_message.payload.split(',')
            self.host_area = payload_array[0]
            i = 1
            while i < len(payload_array):
                self.host_ips.append(payload_array[i])
                i += 1
            #ready to call new function
            self.setupHostConnections()
        else:
        	#invalid message type - can not connect to network
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
        #here, all of the host connections have been set up
        #need to start the listening thread and the work thread now
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
            if(message.type == 'NHST'):
                self.host_ips.append(message.origin)
                new_thread = Thread(target=lambda: self.listenToHost(new_conn_sock))
                new_thread.start()
                self.connections.append(Connection(new_conn_ip, new_conn_sock, new_thread))
            else:
                print('Invalid Message Type received')
        return


    def processWork(self):
        while self.running == True:
            if len(self.work_queue) == 0:
                self.work_queue = ['Do Math', 'Send HUPD', 'Receive All HUPDs']
            else:
                instruction = self.work_queue.pop(0)
                if instruction == 'Do Math' :
                    #run calculations
                elif instruction == 'Send HUPD':
                    #broadcast out this host's HUPD
                elif instruction == 'Receive All HUPDs':
                    #make sure to receive all HUPDs from listening threads
                elif instruction == 'NHST':
                    #run a function to add the new host ip to the list of host ip + add new host connection to the list of connections
                elif instruction == 'LHST':
                    #run a function to remove the lost host from list of host ips + close and remove lost host connection from list of connections
                else:
                    print('Invalid Instruction - skipping...')

        return

    def listenToHost(self, host_sock):
        while self.running == True:
            message = parseMessage(host_sock)
            if message.type == 'HUPD':
                #pass message payload somewhere so they can be used for next calculcations
                self.updates_received.append(message.origin)
                while(self.updated != True):
                    #wait
                    wait = 'wait'
            elif message.type == 'LHST':
                for host_ip in self.host_ips:
                    if host_ip == message.origin:
                        self.host_ips.remove(host_ip)
                #here, host_ip was removed from list of host_ips
                for connection in self.connections:
                    if connection.ip == message.origin:
                        connection.close()
                        self.connections.remove(connection)
                #here, the connection for the host was closed + connection was removed from list of connections
            else:
                print('Invalid message type received')
        return



class Connection():
    def __init__(self, ip, sock, thread ):
        self.ip = ip
        self.host_sock = sock
        self.host_thread = thread

    def close(self):
        #connection close function for closing sockets and threads
        self.host_sock.close()
        self.host_thread.exit()
        print("Host has been disconnected")
