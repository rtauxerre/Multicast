#! /usr/bin/env python3

#
# Multicast Chat Application - Server implementation
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2021 Michaël Roy
#

# External dependencies
import socket

# Multicast address and port
multicast_address = '239.0.0.1'
multicast_port = 10000

# Banner
print( '\nWelcome to the multicast chat receiver from RT Auxerre !')
print( 'Press Ctrl+C to stop the application...\n' )
print( 'Received messages :\n' )

# Create a UDP server socket
with socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) as connection :
	# Setup the multicast group
	connection.setsockopt( socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
		socket.inet_aton( multicast_address ) + socket.inet_aton( '0.0.0.0' ) )
	# Bind the socket
	connection.bind( ( '0.0.0.0', multicast_port ) )
	# Handle exceptions such as Ctrl+C
	try :
		# Receive messages
		while True :
			message, address = connection.recvfrom( 4096 )
			print( '{} : {} > {}'.format( *address, message.decode() ) )
	# Exceptions
	except : pass
