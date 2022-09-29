#! /usr/bin/env python3

#
# Multicast Video Streaming
# https://github.com/rtauxerre/Multicast
# Copyright (c) 2022 Michaël Roy
# usage : $ ./stream.py
#

# External dependencies
import argparse
import os

# Default parameters
video_file = 'big_buck_bunny_720p_h264.ts'
multicast_address = '239.0.0.1'
multicast_port = '5004'
ttl = '10'
dscp = '0x60'

# Command line arguments
parser = argparse.ArgumentParser( description = 'Multicast Video Streaming' )
parser.add_argument( '--video', default=video_file, help='A video file to stream (default: {})'.format( video_file ) )
parser.add_argument( '--address', default=multicast_address, help='Destination address (default: {})'.format( multicast_address ) )
parser.add_argument( '--port', default=multicast_port, help='Destination port (default: {})'.format( multicast_port ) )
parser.add_argument( '--ttl', default=ttl, help='TTL (default: {})'.format( ttl ) )
parser.add_argument( '--dscp', default=dscp, help='DSCP (default: {})'.format( dscp ) )
arguments = parser.parse_args()

# Define the command line
command = 'cvlc ' + arguments.video + ' --sout \'#rtp{dst=' + arguments.address + ',port=' + arguments.port + ',mux=ts,ttl=' + arguments.ttl + '}\' --sout-all --sout-keep --loop --dscp ' + arguments.dscp
print( '\n' + command + '\n' )

# Execute the command to stream
os.system( command )
