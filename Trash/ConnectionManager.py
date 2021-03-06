import socket
import sys
from Message import Message # used for testing
from BroadcastListener import BroadcastListener
class ConnectionManager:
    def __init__(self, time, coord):
        self.time_step = time
        self.host_connection_list = []
        self.coordinator = coord

    def send_update(self, message):
        """
        Given some message, the broadcaster will send this message to all currently
        connected hosts

        param message is the message object to be sent
        param_type  message is a Message object
        """
        for connection in self.host_connection_list:
            connection.sock.send(message.generateByteMessage())

    def add_host_with_address(self, IP_addy, Port_addy):
        """
        A method that is ready to add a host given an IP address and Port address
        Will create a socket with the IP and Port and then add it to host list
        """
        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_sock.connect((IP_addy, Port_addy))
        self.host_connection_list.append(HostConnection(new_sock, IP_addy))
        new_listener = BroadcastListener(self, new_sock)
        #broadcast ACK to serverPC

    def add_host_with_socket(self, sock, ip_address):
        """
        A method that can add a host to the list as a socket Should be mainly used
        during startup when existing Hosts in the network try to connect to this
        host
        """
        self.host_connection_list.append(HostConnection(sock, ip_address))
        #new_listener
        #broadcast ACK to serverPC

    def remove_host(self, ip_address):
        """
        a method to remove a specific host given an IP, will be done after
        ServerPC sends a LoseHost message
        """
        #iterate throught list of host connections
        for host_conn in host_connection_list:
            if host_conn.ip_address == ip_address:
                host_connection_list.remove(host_conn)
                break

class HostConnection:

    def __init__(self,sock, ip):
        self.sock = sock
        self.ip_address = ip


if __name__ == "__main__":
    second_test()
