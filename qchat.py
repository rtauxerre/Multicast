#! /usr/bin/env python3

#
# Multicast Chat Application with Qt interface
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2021 Michaël Roy
#

# External dependencies
import os
import select
import socket
import sys
import time
import threading
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

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
				global window
				window.text_area.append('{}:{} > {}'.format( address[0], address[1], message.decode() ))
			# Temporization
			time.sleep( 0.03 )
		# Close the connection
		connection.close()

#
# Chat client with Qt interface
#
class QChat( QWidget ) :
	# Initialize the window
	def __init__( self ):
		QWidget.__init__( self )
		# Set the window title
		self.setWindowTitle( 'RT Auxerre Multicast Chat' )
		# Text edit to show the received messages
		self.text_area = QTextEdit()
		self.text_area.setFocusPolicy( Qt.NoFocus )
		# Line edit to enter the messages to send
		self.message = QLineEdit()
		# Application layout
		self.layout = QVBoxLayout( self )
		self.layout.addWidget( self.text_area )
		self.layout.addWidget( self.message )
		# Signal to know when a new message is entered
		self.message.returnPressed.connect( self.send_message )
		# Set the Escape key to close the application
		QShortcut( QKeySequence( Qt.Key_Escape ), self ).activated.connect( self.close )
		# Network connection to send the messages
		self.connection = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.connection.setsockopt( socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1 )
	# Send the message through the network
	def send_message( self ) :
		# Send the message through the network
		self.connection.sendto( self.message.text().encode(), ( multicast_address, multicast_port ) )
		# Clear the text input widget
		self.message.clear()
	# Close the widget
	def closeEvent( self, event ) :
		# Close the connection
		self.connection.close()
		# Close the server
		global server
		server.running = False
		# Close main application
		event.accept()

#
# Main application
#
if __name__ == "__main__" :
	# Remove Qt warnings
	os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
	os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
	os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
	os.environ["QT_SCALE_FACTOR"] = "1"
	# Start the server
	server = ChatServer()
	server.start()
	# Start the Qt application
	app = QApplication( [] )
	window = QChat()
	window.show()
	sys.exit( app.exec_() )
