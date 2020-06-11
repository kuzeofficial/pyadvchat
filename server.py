#! /usr/bin/env python
#! -*- coding: utf-8 -*-
# Server TCP Chat

#Autor: Cristian Fonseca Comas
#Author = Cristian Fonseca Comas
#Age = 16
#Date = may 3 of 2019
#A.K.A = Kuze

#This is a server chat used sockets

#Import Library
import socket, select
# Console colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan


#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
	#Do not send the message to master socket and the client who has send us the message
	for socket in CONNECTION_LIST:
		if socket != server_socket and socket != sock :
			try :
				socket.send(message)
			except :
				# broken socket connection may be, chat client pressed ctrl+c for example
				socket.close()
				CONNECTION_LIST.remove(socket)

if __name__ == "__main__":
	#Variable Declaration	
	# List to keep track of socket descriptors
	CONNECTION_LIST = []
	RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
	IPADDR = "0.0.0.0"
	PORT = int(input("PORT: "))
	
	#Create the connection socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# this has no effect, why ?
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		#Bin the socket for 10 connection's
		server_socket.bind((IPADDR, PORT))
		server_socket.listen(10)

		# Add server socket to the list of readable connections
		CONNECTION_LIST.append(server_socket)

		print ("[INFO] Chat server started", IPADDR , "on port ", PORT)

		while 1:
			# Get the list sockets which are ready to be read through select
			read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
			for sock in read_sockets:
				#New connection
				if sock == server_socket:
					# Handle the case in which there is a new connection recieved through server_socket
					sockfd, addr = server_socket.accept()
					CONNECTION_LIST.append(sockfd)
					print (G+"Client (%s, %s) connected" % addr+W)
				
					#broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
			
				#Some incoming message from a client
				else:
					# Data recieved from client, process it
					try:
						#In Windows, sometimes when a TCP program closes abruptly,
						# a "Connection reset by peer" exception will be thrown
						data = sock.recv(RECV_BUFFER)
						if data:
							broadcast_data(sock, "\r"  + data)                
					except KeyboardInterrupt:
						broadcast_data(sock, "Client (%s, %s) is offline" % addr)
						print("Client (%s, %s) is offline" % addr)
						sock.close()
						CONNECTION_LIST.remove(sock)
						server_socket.close()
	except KeyboardInterrupt:
		print (R+"[INFO] Not started server..."+W)
		server_socket.close()
	

			

