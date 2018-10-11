import Message
import threading


class Host:

    def __init__(self, ip, port, server_ip):
        self.ip = ip
        self.port = port
        self.serverPC_ip = server_ip
        self.host_ips = []
        self.conn_sockets = []


    def listening_port(self):
        #this will be for the port that constantly listens for new connections
        #create a new thread here for running this, or call the thread elsewhere to run this functions
        listening_socket = socket.socket(socket.AF_INET, aocket.SOCK_STREAM)
        listening_socket.bind((self.ip, 9090))
        listening_socket.listen(1)
        while True:
            new_conn, new_conn_addr = listening_socket.accept()
            #wait for a NHST message from the new connect
            message = parseMessage(new_conn)
            if(message.type == 'NHST'):
                #deal with NHST
                self.host_ips.append(message.origin)
                #add the new_conn socket to the list of conn_sockets
                
            else:
                print('Invalid Message Type received')

    def run(self):
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSock.bind((self.ip, self.port))
        clientSock.connect((self.serverPC_ip, 9090))
        message = Message('CREQ', self.ip, '\0')
        clientSock.sendall(message.generateByteMessage())
        response_message = self.parseMessage(clientSock)
        if(response_message.type == 'OKAY'):
        	print('OKAY message received')
          payload_array = response_message.payload.split(',')
          self.host_area = payload_array[0]
          i = 1
          while i < len(payload_array):
          	self.host_ips[i-1] = payload_array[i]
          	i += 1
          #ready to call new function
          self.setupHostConnections()

        else:
        	#invalid message type - can not connect to network
            print('Invalid message type received')

		def setupHostConnections(self):
    		for hosts in host_ips:
        		#create socket for currHost
        		hostSocket = socket.socket(AF_INET, SOCK_STREAM)
                hostSocket.connect((hosts, 9090))
                newHostMsg = Message("NHST", self.ip, self.host_area)
                newHostMsg.generateByteMessage()
                hostSocket.sendall(newHostMsg)
                #MAKE CONNECTION OBJECT WITH BELOW
                    #create thread for listening to connection
                    #start thread
                    #Add socket and thread to list for clean disconnect and IP
                #start thread with target processWork

class Connection(thread.threading):
    def __init__(self,ip, socket, thread ):
        self.ip = ip
        self.hostSock = socket
        self.hostThread = thread

    def close(self):
        #connection close function for closing sockets and threads
        self.hostSock.close()
        self.hostThread.exit()
        print("Host has been disconnected")
