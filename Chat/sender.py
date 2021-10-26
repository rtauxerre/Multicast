#! /usr/bin/env python3

#
# Multicast Chat Application - Client implementation
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2021 Michaël Roy
#

# External dependencies
import socket

# Multicast address and port
multicast_address = '239.0.0.1'
multicast_port = 10000

# Banner
print( '\nWelcome to the multicast chat sender from RT Auxerre !')
print( 'Press Ctrl+C to stop the application...\n' )
print( 'Send a message :\n' )

# Create a UDP client socket
with socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) as connection :
	# Handle exceptions such as Ctrl+C
	try :
		while True :
			# Get the message from console input
			message = input( '> ' )
			# Send the message to the multicast address and port
			connection.sendto( message.encode(), ( multicast_address, multicast_port ) )
	# Exception
	except : pass
