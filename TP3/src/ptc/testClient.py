# coding: utf-8

from ptc import * 
from time import sleep

def createClient():
	client = PTCClient('127.0.0.1', 45454)
	client.connect('127.0.0.1', 12345)
	return client

def createServer():
	server = PTCServer('127.0.0.1', 12345) 
	server.accept()
	return server
