#! /usr/bin/env python3

#
# Multicast Chat Application
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2021 Michaël Roy
# Inspired by evchat : https://github.com/EvanKuhn/evchat
#

# External dependencies
import curses
import socket
import threading
import time

# Multicast address and port
multicast_address = '239.0.0.1'
multicast_port = 10000

# Message class
class Message :
	def __init__( self, source = None, text = None ) :
		self.source = source
		self.text = text

# Chat Server
def Server( parent ) :
	# Create a UDP socket
	with socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) as connection :
		# Set up the server connection
		connection.setsockopt( socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
				socket.inet_aton( multicast_address ) + socket.inet_aton( '0.0.0.0' ) )
		# Bind the socket
		connection.bind( ( '0.0.0.0', multicast_port ) )
		# Continuously read client message
		while True :
			# Wait for a message
			message, address = connection.recvfrom( 4096 )
			# Print the message
			parent.history.AppendMessage( Message( address, message.decode() ) )
			# Update the UI
			parent.Redraw()

# Screen layout
class Layout :
	# Determine the terminal size, and the size of each window
	def __init__( self, screen ) :
		# Get terminal size
		rows, cols = screen.getmaxyx()
		# Calculate dimensions of each window
		TITLE_ROWS = 3
		PROMPT_ROWS = 3
		self.title_rows         = TITLE_ROWS
		self.title_cols         = cols
		self.title_start_row    = 0
		self.title_start_col    = 0
		self.history_rows       = rows - TITLE_ROWS - PROMPT_ROWS
		self.history_cols       = cols
		self.history_start_row  = TITLE_ROWS
		self.history_start_col  = 0
		self.prompt_rows        = PROMPT_ROWS
		self.prompt_cols        = cols
		self.prompt_start_row   = rows - PROMPT_ROWS
		self.prompt_start_col   = 0

# Title window
class Title :
	def __init__( self, layout ) :
		title = "RT Auxerre Multicast Chat"
		self.window = curses.newwin( layout.title_rows, layout.title_cols,
			layout.title_start_row + 1, layout.title_start_col )
		self.window.addstr( 0, int( ( layout.title_cols - len( title ) ) / 2 ), title, curses.A_BOLD )
	def Redraw( self ) :
		self.window.refresh()

# History window
class History :
	def __init__( self, layout ) :
		self.messages = []
		self.window = curses.newwin( layout.history_rows, layout.history_cols,
			layout.history_start_row, layout.history_start_col )
		# Because we have a border and some padding, the number of visible rows is fewer
		self.visible_rows = layout.history_rows - 4
	def AppendMessage( self, msg ) :
		# Append a Message object to the history. Does not redraw.
		self.messages.append( msg )
	def Redraw( self ) :
		self.window.clear()
		self.window.border( 0 )
		# Draw the last N messages, where N is the number of visible rows
		row = 2
		for msg in self.messages[ -self.visible_rows : ] :
			self.window.move( row, 3 )
			self.window.addstr( '{}:{} > '.format( *msg.source ), curses.A_BOLD )
			self.window.addstr( msg.text )
			row += 1
		self.window.refresh()

# Prompt Window
class Prompt :
	def __init__( self, layout ) :
		self.window = curses.newwin( layout.prompt_rows, layout.prompt_cols,
			layout.prompt_start_row, layout.prompt_start_col )
		self.window.keypad( 1 )
		self.window.border( 0 )
		self.window.move( 1, 1 )
		self.window.addstr( ' > ', curses.A_BOLD )
	# Get an input string from the user
	def GetMessage( self ):
		return self.window.getstr()
	# Redraw the prompt window
	def Redraw( self ) :
		self.window.clear()
		self.window.border( 0 )
		self.window.move( 1, 1 )
		self.window.addstr( ' > ', curses.A_BOLD )
		self.window.refresh()

# Main application
class ChatApp :
	def __init__( self ) :
		# Catch exceptions
		try:
			# Initialize curses
			self.screen = curses.initscr()
			curses.cbreak()
			self.screen.keypad( 1 )
			# Define the screen layout
			self.layout = Layout( self.screen )
			# Initialize all curses-based objects
			self.title   = Title( self.layout )
			self.history = History( self.layout )
			self.prompt  = Prompt( self.layout )
			# Start the server thread to receive messages
			threading.Thread( target=Server, args=(self,), daemon=True ).start()
			# Open a client connection to send message
			self.connection = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
			# Run the main loop
			while True:
				# Update the UI
				self.Redraw()
				# Get input
				text = self.prompt.GetMessage()
				# Continue if the message is empty
				if not text : continue
				# Send the message
				self.connection.sendto( text, ( multicast_address, multicast_port ) )
				# Wait a moment (curses issue)
				time.sleep( 0.1 )
		# Catch the exceptions
		except : pass
		# Close the application nicely
		finally :
			# Close client connection
			self.connection.close()
			# Stop curses
			curses.nocbreak()
			self.screen.keypad(0)
			self.screen = None
			curses.endwin()
	# Redraw the main screen
	def Redraw( self ) :
		self.screen.refresh()
		self.title.Redraw()
		self.history.Redraw()
		self.prompt.Redraw()

# Main application
if __name__ == '__main__' :
	# Run the app
	app = ChatApp()
	