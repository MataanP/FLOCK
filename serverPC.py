import sys
import socket
from Message import Message

class serverPC:

	def __init__(self):
		self.servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host_addrs = []
		self.max_xcoord = 0

	def parseMessage(self, sock):
		try:
			#parse the type
			msg = b''
			while True:
				byte = sock.recv(1)
				if len(byte) == 0:
					raise ConnectionError('Socket is closed')
				if byte == b'\n':
					break
				msg += byte
			datatype = msg.decode()
			#parse the origin address
			msg = b''
			while True:
				byte = sock.recv(1)
				if len(byte) == 0:
					raise ConnectionError('Socket is closed')
				if byte == b'\n':
					break
				msg += byte
			origin = msg.decode()
			#parse the payload
			msg = b''
			while True:
				byte = sock.recv(1)
				if len(byte) == 0:
					raise ConnectionError('Socket is closed')
				if byte == b'\n':
					break
				msg += byte
			payload = msg.decode()
			#create the message
			return Message(datatype, origin, payload)
		except:
			#Error reading from socket
			return None


	def run(self, ip_address, port, allowedClients):
		self.servSock.bind((ip_address, int(port)))
		self.servSock.listen(1)
		while True:
			conn, (client_ip, client_port) = self.servSock.accept()
			x = 0
			for client in allowedClients:
				#check if incoming connection IP is allowed on to the network
				print("Client info", client)
				if client == client_ip:
					print("This client is allowed to connect")
					x += 1
					break
			if x == 0:
				print("This host does not have permission to connect with this network")
				conn.close()
			else:
				#check if the host sent the proper CREQ message
				message = self.parseMessage(conn)
				if message.type == 'CREQ':
					#Payload checking list of host addrs
					print('cool - received CREQ message')
					#Allocate bird area call outside area function
					payload = str(self.max_xcoord) + ',' + ','.join(self.host_addrs)
					message = Message("OKAY", ip_address, payload)
					#send okay message containing the list of other connected IPs on the network
					conn.send(message.generateByteMessage())
					new_message = self.parseMessage(conn)
					if new_message.type == 'LHST':
						#format and send new area message
						payload_array = new_message.payload.split(',')
						print(len(payload_array))
						if len(payload_array) > 0:
							#Remove the disconnected IP from the list of currently connected hosts
							for dead_ip in payload_array:
								if(dead_ip != ''):
									self.host_addrs.remove(dead_ip)
						conn.close()
						self.max_xcoord += 50
						self.host_addrs.append(client_ip)
					else:
						print('Invalid message type received - LHST expected, message of type ' + message.type + ' received.')
						conn.close()
				else:
					print('Invalid message type received - CREQ expected, message of type ' + message.type + ' received.')
					conn.close()

	def readConfig(self):
		confFileName = sys.argv[1]
		file = open(confFileName, 'r')
		hostChecker = []
		serverAddr = []
		for line in file:
			addr = line.split()
			if addr[0] == 'addr':
				#gather all the allowed host addresses
				hostChecker.append(addr[1])
			elif addr[0] == 'serverAddr':
				serverAddr.append(line)
		server = serverAddr[0].split()
		print(server[1])
		self.run(server[1], server[2], hostChecker)

serverPC().readConfig()
