#! /bin/bash

cvlc $1 --sout '#rtp{dst=239.0.0.1,mux=ts,ttl=10}' --sout-all --sout-keep --dscp 0x80 --loop
