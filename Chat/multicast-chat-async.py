#! /usr/bin/env python3

#
# Multicast Chat Application
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2021 Michaël Roy
# usage : $ ./multicast-chat.py
#

# External dependencies
import asyncio
import signal
import socket
import threading
import sys

# Multicast address and port
MULTICAST_ADDRESS = '239.0.0.1'
MULTICAST_PORT = 10000

# Chat server protocol
class ChatServer :
	# Connection
	def connection_made( self, transport ) :
		self.transport = transport
		self.transport.get_extra_info('socket').setsockopt( socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
			socket.inet_aton( MULTICAST_ADDRESS ) + socket.inet_aton( '0.0.0.0' ) )
	# Message reception
	def datagram_received( self, message, address ) :
		print( '\n{}:{} > {}'.format( *address, message.decode() ) )
		sys.stdout.write('> ')
		sys.stdout.flush()

# Start the server
def chat_server_start() :
	# Start a new event loop
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop( loop )
	# Create the server
	server = loop.create_datagram_endpoint( lambda : ChatServer(), local_addr = ( '0.0.0.0', MULTICAST_PORT ) )
	# Start the server
	loop.run_until_complete( server )
	loop.run_forever()

# Main application
if __name__ == '__main__' :
	print( '\nPress ^C to stop the server...\n' )
	# Start the server thread to receive messages
	threading.Thread( target=chat_server_start, daemon=True ).start()
	try :
		# Create a UDP socket
		with socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) as connection :
			# Continuously read the messages from input and send them
			while True :
				# Get the message from input
				message = input( '> ' )
				# Check if the message is empty
				if not message : continue
				# Send the message through the network
				connection.sendto( message.encode(), ( MULTICAST_ADDRESS, MULTICAST_PORT ) )
	except KeyboardInterrupt :
		pass
