#! /usr/bin/env python3

#
# Multicast Chat Application - Server implementation
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2022 Michaël Roy
# usage : $ ./receiver-async.py
#

# External dependencies
import asyncio
import socket

# Multicast address and port
multicast_address = '239.0.0.1'
multicast_port = 10000

# Chat server protocol
class ChatServer :
	# Connection
	def connection_made( self, transport ) :
		self.transport = transport
		self.transport.get_extra_info('socket').setsockopt( socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
			socket.inet_aton( multicast_address ) + socket.inet_aton( '0.0.0.0' ) )
	# Message reception
	def datagram_received( self, message, address ) :
		print( '{} : {} > {}'.format( *address, message.decode() ) )

# Main application
if __name__ == '__main__' :
	print( '\nPress ^C to stop the server...\n' )
	loop = asyncio.get_event_loop()
	server = loop.create_datagram_endpoint( lambda: ChatServer(), local_addr=('::', multicast_port) )
	loop.run_until_complete( server )
	try :
		loop.run_forever()
	except KeyboardInterrupt :
		pass
