
class Host:

    def __init__(self, ip, port, server_ip):
        self.ip = ip
        self.port = port
        self.serverPC_ip = server_ip
        self.host_ips = []
        self.conn_sockets = []

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
