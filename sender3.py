#! /usr/bin/env python3

#
# Multicast Chat Application - Client implementation
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2021 Michaël Roy
# usage : $ ./sender3.py message
#

# External dependencies
import socket
import sys

# Check the message
if len( sys.argv ) > 1 : message = sys.argv[ 1 ]
else : print( 'Message missing...' ); exit( 1 )

# Multicast address
multicast_address = '239.0.0.1'

# Multicast port
multicast_port = 10000

# Create a UDP socket
with socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) as connection :
	# Send the message to the multicast address and port
	connection.sendto( message.encode(), ( multicast_address, multicast_port ) )

