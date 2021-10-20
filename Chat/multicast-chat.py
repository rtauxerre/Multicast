#! /usr/bin/env python3

#
# Multicast Chat Application
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2021 Michaël Roy
# usage : $ ./multicast-chat.py
#

# External dependencies
import select
import socket
import time
import threading

# Multicast address
multicast_address = '239.0.0.1'

# Multicast port
multicast_port = 10000

#
# Chat Server
#
class ChatServer( threading.Thread ) :
	# Server main loop
	def run( self ) :
		# Set up the server connection
		connection = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		connection.setsockopt( socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
				socket.inet_aton( multicast_address ) + socket.inet_aton( '0.0.0.0' ) )
		connection.bind( ( '0.0.0.0', multicast_port ) )
		# Continuously read client message
		self.running = True
		while self.running :
			# Wait for a message
			ready, _, _ = select.select( [ connection ], [], [], 0 )
			# Message received
			if ready :
				# Read the message
				message, address = connection.recvfrom( 255 )
				# Print the message
				print( 'Received from {} : {} > {}'.format( *address, message.decode() ) )
			# Temporization
			time.sleep( 0.1 )
		# Close the connection
		connection.close()

#
# Chat client
#
class ChatClient( threading.Thread ) :
	# Client main loop
	def run( self ) :
		# Create a UDP socket
		connection = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		# Continuously read the messages from input and send them
		self.running = True
		while self.running :
			# Get the message from input
			message = input( '> ' )
			# Check if the message is empty
			if not message : continue
			# Check if the message is the 'quit' command
			if message == "quit" :
				# Stop the client
				self.running = False
				# Get the server
				global server
				# Stop the server
				server.running = False
				break
			# Send the message through the network
			connection.sendto( message.encode(), ( multicast_address, multicast_port ) )
			# Temporization
			time.sleep( 0.1 )
		# Close the connection
		connection.close()

#
# Main application
#
if __name__ == '__main__' :
	# Banner
	print( '\nWelcome to the multicast chat application from RT Auxerre !')
	print( 'Type \'quit\' to stop the application...\n' )
	# Start the server
	server = ChatServer()
	server.start()
	# Start the client
	client = ChatClient()
	client.start()
