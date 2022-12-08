#! /usr/bin/env python3

#
# Multicast Chat Application
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2021 Michaël Roy
# usage : $ ./multicast-chat.py
#

# External dependencies
import signal
import socket
import threading

# Multicast address and port
MULTICAST_ADDRESS = 'FF08::b0b'
MULTICAST_PORT = 10000

# Chat Server
def Server() :
	# Create a UDP socket
	with socket.socket( socket.AF_INET6, socket.SOCK_DGRAM ) as connection :
		# Set up the server connection
		connection.setsockopt( socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP,
				socket.inet_pton( socket.AF_INET6, MULTICAST_ADDRESS ) + socket.inet_pton( socket.AF_INET6, '::' ) )
		# Bind the socket
		connection.bind( ( '', MULTICAST_PORT ) )
		# Continuously read client message
		while True :
			# Wait for a message
			message, address = connection.recvfrom( 4096 )
			# Print the message
			print( '{} : {} > {}'.format( *address, message.decode() ) )

# Chat client
def Client() :
	# Create a UDP socket
	with socket.socket( socket.AF_INET6, socket.SOCK_DGRAM ) as connection :
		# Continuously read the messages from input and send them
		while True :
			# Get the message from input
			message = input( '> ' )
			# Check if the message is empty
			if not message : continue
			# Send the message through the network
			connection.sendto( message.encode(), ( MULTICAST_ADDRESS, MULTICAST_PORT ) )

# Main application
if __name__ == '__main__' :
	# Banner
	print( '\nWelcome to the multicast chat application from RT Auxerre !')
	print( 'Press Ctrl+C to stop the application...\n' )
	# Handle exceptions such as Ctrl+C
	try :
		# Start the server
		threading.Thread( target=Server, daemon=True ).start()
		# Start the client
		threading.Thread( target=Client, daemon=True ).start()
		# Wait for a signal (such as KeybordInterrupt)
		signal.pause()
	# Exceptions : quit the program
	except : pass
