import socket
import sys
from Message import Message
class ConnectionManager:
    def __init__(self, time, coord):
        self.time_step = time
        self.host_socket_list = []
        self.coordinator = coord

    def send_update(self, message):
        """
        Given some message, the broadcaster will send this message to all currently
        connected hosts

        param message is the message object to be sent
        param_type  message is a Message object
        """
        for socket in self.host_socket_list:
            socket.send(message.generateByteMessage())

    def add_host_with_address(self, IP_addy, Port_addy):
        """
        A method that is ready to add a host given an IP address and Port address
        Will create a socket with the IP and Port and then add it to host list
        """
        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_sock.connect((IP_addy, Port_addy))
        self.host_socket_list.append(new_sock)
        #new_listener = BroadcastListener(self.coord, self.time_step, new_sock)
        return new_sock #only used for testing

    def add_host_with_socket(self, socket):
        """
        A method that can add a host to the list as a socket Should be mainly used
        during startup when existing Hosts in the network try to connect to this
        host
        """
        self.host_socket_list.append(socket)

def main():
    manager = ConnectionManager(4,1)
    manager.add_host_with_address("172.16.135.204",9090)
    manager.send_update(Message("MSG","1231","ashdalej"))
if __name__ == "__main__":
    main()
