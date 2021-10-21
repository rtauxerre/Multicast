#! /usr/bin/env python3

#
# Multicast Chat Application - Client implementation
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2021 Michaël Roy
# usage : $ ./sender.py
#

# External dependencies
import socket

# Multicast address and port
multicast_address = '239.0.0.1'
multicast_port = 10000

# Handle exceptions such as Ctrl+C
try :
	# Create a UDP socket
	connection = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
	while True :
		# Get the message from console input
		message = input( '> ' )
		# Send the message to the multicast address and port
		connection.sendto( message.encode(), ( multicast_address, multicast_port ) )
# Exceptions
except : pass
# Close the connection
finally : connection.close()
