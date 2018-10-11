import sys
import socket

class serverPC:

	def __init__(self):
		self.servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host_addrs = []


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

#TO DO
#check IP
#allocating space (pseudoCode)
#Be listening for new connections
#respond to new host w/ # of other hosts on network
#send NHST message w/ NewHost addr as payload to all existing hosts
#create new host message
	def run(self, address, port, allowedClients):
		#create recieving addr
		addr = address, int(port)
		#Bind socket to addr
		self.servSock.bind(addr)
		self.servSock.listen(1)
		#Accept connection
		while True:
			conn, (client_ip, client_port) = self.servSock.accept()
			x = 0
			for client in allowedClients:
				print("Client info", client)
				if client == client_ip:
					print("This client is allowed to connect")
					x += 1
					break
			if x == 0:
				print("This host does not have permission to connect with this network")
				conn.close()
			message = self.parseMessage(conn)
			if message.type == 'CREQ':
				#Payload checking list of host addrs
				print('cool - received CREQ message')
				#Allocate bird area call outside area function
				payload = "Bird Area," + ','.join(self.host_addrs)
				message = Message("OKAY", addr, payload)
				conn.send(message.generateByteMessage())
				conn.close()
				self.host_addrs.append(client_ip)
				#serverPC received CREQ message from new connection
				#now, need to send out NHST message to all existing hosts
				#once all existing hosts have responded with ACKN, send OKAY message to new connection
				#add the new connection to the list of host connections
			else:
				print('Invalid message type received - CREQ expected, message of type ' + message.type + ' received.')
				conn.close()
			#still gotta wait for the CREQ message


	def readConfig(self):
		print("here")
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
		self.run(server[1], server[2], hostChecker)

serverPC().readConfig()
