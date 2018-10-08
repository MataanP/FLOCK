import socket
def Class BroadcastManager:
    # data structure declaration for storing all the Host Connections, Could either store sockets or ip and port
    #ListenerDataStructure
    def __init__(self, time):
        self.time_step = time
        self.host_list = []

    def send_update(self, message):
        while: #some conditional, maybe this is a thread, not sure
            #for socket in dataStructure
                socket.send(message.encode())

    def add_host(self, IP_addy, Port_addy):
        new_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        new_sock.connect((IP_addy, Port_addy))
        #data structure.add(new_sock)
        new_listener = BroadcastListener(self.time_step, new_sock)
        #ListenerDataStructure.add()


    # i need to be able to receive information from within this host, and broadcast it to all hosts
    # i need to be able to receive information from the sockets(threading), and sent it to this host
