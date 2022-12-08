#
# Multicast Chat Application
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2022 Michaël Roy
# Inspired by evchat : https://github.com/EvanKuhn/evchat
#

# External dependencies
import signal
import socket
import threading

# Multicast address and port
MULTICAST_ADDRESS4 = '239.0.0.1'
MULTICAST_ADDRESS6 = 'FF08::1'
MULTICAST_PORT = 10000

# Application title
APP_TITLE = 'RT Auxerre Multicast Chat'

# Chat Server with IPv4
def ServerIPv4() :
	# Create a UDP socket
	with socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) as connection :
		# Set up the server connection
		connection.setsockopt( socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
				socket.inet_aton( MULTICAST_ADDRESS4 ) + socket.inet_aton( '0.0.0.0' ) )
		# Bind the socket
		connection.bind( ( '0.0.0.0', MULTICAST_PORT ) )
		# Continuously read client message
		while True :
			# Wait for a message
			message, address = connection.recvfrom( 4096 )
			# Print the message
			print( '{} > {}'.format( address[0], message.decode() ) )

# Chat Server with IPv6
def ServerIPv6() :
	# Create a UDP socket
	with socket.socket( socket.AF_INET6, socket.SOCK_DGRAM ) as connection :
		# Set up the server connection
		connection.setsockopt( socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP,
				socket.inet_pton( socket.AF_INET6, MULTICAST_ADDRESS6 ) + socket.inet_pton( socket.AF_INET6, '::' ) )
		# Bind the socket
		connection.bind( ( '', MULTICAST_PORT ) )
		# Continuously read client message
		while True :
			# Wait for a message
			message, address = connection.recvfrom( 4096 )
			# Send the message to the main application
			print( '{} > {}'.format( address[0], message.decode() ) )

# Chat client with IPv4
def ClientIPv4() :
	# Create a UDP socket
	with socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) as connection :
		# Continuously read the messages from input and send them
		while True :
			# Get the message from input
			message = input( '> ' )
			# Check if the message is empty
			if not message : continue
			# Send the message through the network
			connection.sendto( message.encode(), ( MULTICAST_ADDRESS4, MULTICAST_PORT ) )

# Chat client with IPv6
def ClientIPv6() :
	# Create a UDP socket
	with socket.socket( socket.AF_INET6, socket.SOCK_DGRAM ) as connection :
		# Continuously read the messages from input and send them
		while True :
			# Get the message from input
			message = input( '> ' )
			# Check if the message is empty
			if not message : continue
			# Send the message through the network
			connection.sendto( message.encode(), ( MULTICAST_ADDRESS6, MULTICAST_PORT ) )

# Start
def start_servers() :
	# Start the servers
	threading.Thread( target=ServerIPv4, daemon=True ).start()
#	threading.Thread( target=ServerIPv6, daemon=True ).start()


# Main application
if __name__ == '__main__' :
	# Banner
	print( '' )
	print( APP_TITLE )
	print( 'Press Ctrl+C to stop the application...\n' )
	# Handle exceptions such as Ctrl+C
	try :
#		start_servers()
#		threading.Thread( target=ServerIPv4, daemon=True ).start()
		threading.Thread( target=ServerIPv6, daemon=True ).start()
		# Start the client
#		threading.Thread( target=ClientIPv4, daemon=True ).start()
		threading.Thread( target=ClientIPv6, daemon=True ).start()
		# Wait for a signal (such as KeybordInterrupt)
		signal.pause()
	# Exceptions : quit the program
	except : pass
