import sys
sys.path.append('c:\python27\lib')
import xmlrpclib
from time import time
import json

__author__ = 'Joseph Moster'

server = xmlrpclib.ServerProxy('http://127.0.0.1:9001')
print 'Server Info: {}'.format(server.server_info())


def timing(rate):
    """
    Timing Generator, creates delays to achieve the given loop frequency
    Args:
        rate: Rate in Hertz
    """
    next_time = time()
    while True:
        next_time += 1.0 / rate
        delay = int((next_time - time()) * 1000)
        if delay > 0:
            Script.Sleep(delay)
        yield


while True:
    for _ in timing(rate=15):
        try:
            
            server.telemetry(float(cs.lat), float(cs.lng), float(cs.alt), float(cs.groundcourse))
            print json.dumps(server.server_info())
        except:
            print "error"
