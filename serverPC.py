import sys
import threading
import socket

class serverPC:

	def __init__(self):
		self.servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#TODO
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
			print("here")
			(conn, clientAddr) = self.servSock.accept()
			print(clientAddr)
			x = 0
			for client in allowedClients:
				print("Client info", client)
				if client == clientAddr:
					print("This client is allowed to connect")
					x += 1
					break
			if x == 0:
				print("This host does not have permission to connect with this network")
				conn.close()
			#Read incoming data
			while True:
				msg = conn.recv(1024)
				print(len(msg))
				#check ip with conf file
				print("Attempted connection from: ", clientAddr)

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
				addressTuple = (addr[1], int(addr[2]))
				hostChecker.append(addressTuple)
			elif addr[0] == 'serverAddr':
				serverAddr.append(line)
		server = serverAddr[0].split()
		self.run(server[1], server[2], hostChecker)

serverPC().readConfig()
