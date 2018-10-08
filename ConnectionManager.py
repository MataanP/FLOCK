import socket
class ConnectionManager:
    def __init__(self, time):
        self.time_step = time
        self.host_socket_list = []

    def send_update(self, message):
        """
        Given some message, the broadcaster will send this message to all currently
        connected hosts

        param message is the message object to be sent
        param_type  message is a Message object
        """
        for socket in self.host_socket_list:
            socket.send(message.generateByteMessage())

    def add_host(self, IP_addy, Port_addy):
        new_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        new_sock.connect((IP_addy, Port_addy))
        #data structure.add(new_sock)
        new_listener = BroadcastListener(self.time_step, new_sock)
        #ListenerDataStructure.add()


    # i need to be able to receive information from within this host, and broadcast it to all hosts
    # i need to be able to receive information from the sockets(threading), and sent it to this host
