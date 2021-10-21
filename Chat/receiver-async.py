#! /usr/bin/env python3

#
# Multicast Chat Application - Server implementation
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2021 Michaël Roy
# usage : $ ./receiver.py
#

# External dependencies
import asyncio
import socket

# Multicast address and port
multicast_address = '239.0.0.1'
multicast_port = 10000


class EchoServerProtocol :
	def connection_made( self, transport ) :
		self.transport = transport
		self.transport.get_extra_info('socket').setsockopt( socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
			socket.inet_aton( multicast_address ) + socket.inet_aton( '0.0.0.0' ) )
	def datagram_received( self, message, address ) :
		print( '{} : {} > {}'.format( *address, message.decode() ) )

async def main() :
	# Get a reference to the event loop as we plan to use low-level APIs.
	loop = asyncio.get_running_loop()
	# One protocol instance will be created to serve all client requests.
	transport, protocol = await loop.create_datagram_endpoint(
		lambda: EchoServerProtocol(),
		local_addr=('0.0.0.0', multicast_port) )
	try:
		await asyncio.sleep(3600) # Serve for 1 hour.
	finally:
		transport.close()

asyncio.run( main() )