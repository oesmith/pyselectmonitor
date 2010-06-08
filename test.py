#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by Oliver Smith on 2010-01-17.
Copyright (c) 2010 Oliver Smith. All rights reserved.
"""
import time

from reader.file_output import FileOutput
from subaru import SelectMonitor

def main():
    fo = FileOutput('log.txt')
    ssm = SelectMonitor('/dev/tty.usbserial-A6008srP', fo.callback)
    time.sleep(0.1)
    ssm.stop()
    time.sleep(0.3)
    ssm.read(0)
    time.sleep(0.1)
    ssm.get_rom_id()
    time.sleep(0.1)
    ssm.stop()
    #print "press a key to stop harvesting"
    #raw_input()
    #ssm.stop()
    time.sleep(0.1)
    ssm.close()


if __name__ == '__main__':
    main()

