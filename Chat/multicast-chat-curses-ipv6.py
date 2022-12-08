#! /usr/bin/env python3

#
# Multicast Chat Application
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2022 Michaël Roy
# Inspired by evchat : https://github.com/EvanKuhn/evchat
#

# External dependencies
import curses
import socket
import threading
import time

# Multicast address and port
MULTICAST_ADDRESS = 'FF08::1'
MULTICAST_PORT = 10000

# Application title
APP_TITLE = 'RT Auxerre Multicast Chat'

# Chat Server
def Server( new_message_callback ) :
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
			# Send the message to the main application
			new_message_callback( ( address[0], message.decode() ) )

# Main application
class ChatApp :
	# Determine the terminal size, and the size of each window
	def __init__( self ) :
		# Initialize curses
		self.screen = curses.initscr()
		curses.cbreak()
		self.screen.keypad( 1 )
		# Received messages
		self.messages = []
		# Setup the screen interface
		self.SetupInterface()
		# Start the server thread to receive messages
		threading.Thread( target=Server, args=(self.ReceiveMessage,), daemon=True ).start()
		# Open a client connection to send message
		with socket.socket( socket.AF_INET6, socket.SOCK_DGRAM ) as connection :
			# Catch exceptions
			try :
				# Run the main loop
				while True:
					# Update the UI
					self.Redraw()
					# Get input
					text = self.prompt.getstr()
					# Continue if the message is empty
					if not text : continue
					# Send the message
					connection.sendto( text, ( MULTICAST_ADDRESS, MULTICAST_PORT ) )
					# Wait a moment (curses issue)
					time.sleep( 0.1 )
			# Catch the exceptions
			except : pass
		# Stop curses
		curses.nocbreak()
		self.screen.keypad(0)
		self.screen = None
		curses.endwin()
	# Setup the console interface
	def SetupInterface( self ) :
		# Get terminal size
		screen_height, screen_width = self.screen.getmaxyx()
		# Define the height of each window
		title_height = 3
		prompt_height = 5
		history_height = screen_height - title_height - prompt_height - 2
		# Title window
		self.title = curses.newwin( title_height, screen_width - 2, 0, 1 )
		self.title.addstr( 1, int( ( screen_width - len( APP_TITLE ) ) / 2 ), APP_TITLE, curses.A_BOLD )
		# History window
		self.history = curses.newwin( history_height, screen_width - 2, title_height, 1 )
		# Save the number of visible rows (history window height - border - padding ) 
		self.history_visible_rows = history_height - 2 - 2
		#Prompt window
		self.prompt = curses.newwin( prompt_height, screen_width - 2, screen_height - prompt_height - 1, 1 )
	# Redraw the screen
	def Redraw( self ) :
		# Refresh the screen
		self.screen.erase()
		# Refresh the title
		self.title.refresh()
		# Refresh the chat history
		self.history.erase()
		self.history.border( 0 )
		self.history.addstr( 0, 1, ' Message received ', curses.A_BOLD )
		# Draw the last N messages, where N is the number of visible rows
		row = 2
		for address, message in self.messages[ -self.history_visible_rows : ] :
			self.history.move( row, 3 )
			self.history.addstr( '{} > '.format( address ), curses.A_BOLD )
			self.history.addstr( message )
			row += 1
		self.history.refresh()
		# Refresh the prompt
		self.prompt.erase()
		self.prompt.border( 0 )
		self.prompt.addstr( 0, 1, ' Send a message ', curses.A_BOLD )
		self.prompt.addstr( 2, 2, ' > ', curses.A_BOLD )
		self.prompt.refresh()
	# Append a message to the chat history
	def ReceiveMessage( self, msg ) :
		self.messages.append( msg )
		self.Redraw()

# Main application
if __name__ == '__main__' :
	# Run the app
	app = ChatApp()