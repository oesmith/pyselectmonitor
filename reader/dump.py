#!/usr/bin/env python
# encoding: utf-8
"""
dump.py

Created by Oliver Smith on 2010-01-17.
Copyright (c) 2010 Oliver Smith. All rights reserved.
"""

from datetime import datetime
from optparse import OptionParser
import struct
import time

from subaru import SelectMonitor, SELECT_MONITOR_FIELDS

buf = ""
start = 0x7
stop = 0x22
ssm = None
log = open('logs/%s.txt' % (datetime.now().isoformat()), 'w')

def dump(data):
    global start
    global stop
    global log
    t = datetime.now().isoformat()
    log.write('%s [%d-%d] %s\n' % (t, start, stop, 
                                 " ".join(["%02x" % ord(d) for d in data])))
    print t
    for index in range(len(data)):
        if start+index in SELECT_MONITOR_FIELDS:
            name,conv,units = SELECT_MONITOR_FIELDS[start+index]
            print name, conv(ord(data[index])), units


def callback(data):
    global buf
    global ssm
    global start
    global stop
    # append the data to the buffer
    buf += data
    if len(buf) < 3:
        return
    # chop off any crap from the start
    while struct.unpack("!H", buf[:2])[0] != start:
        if len(buf) < 3:
            return
        buf = buf[1:]
    # check to see if we have a full buffer and process it
    datalen = stop - start + 3
    if len(buf) >= datalen:
        dump(buf[2:datalen])
        buf = buf[datalen:]


def main():
    global start
    global stop
    global ssm
    parser = OptionParser()
    parser.add_option("-s", "--start", dest="start", type="int", default=0x7,
                      help="Starting location", metavar="START")
    parser.add_option("-S", "--stop", dest="stop", type="int", default=0x22,
                      help="Stopping location", metavar="STOP")
    (options, args) = parser.parse_args()
    start = options.start
    stop = options.stop
    ssm = SelectMonitor('/dev/tty.usbserial-A6008srP', callback)
    time.sleep(0.1)
    ssm.stop()
    time.sleep(0.3)
    ssm.read(start, stop-start)
    raw_input()
    ssm.stop()
    ssm.close()


if __name__ == '__main__':
	main()

