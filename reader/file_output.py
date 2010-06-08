#!/usr/bin/env python
# encoding: utf-8
"""
file_output.py

Created by Oliver Smith on 2010-01-17.
Copyright (c) 2010 Oliver Smith. All rights reserved.
"""

import datetime

class FileOutput(object):
    """
    An object for logging SSM data to a file.
    """
    
    def __init__(self, filename):
        """
        ctor.
        """
        self.file = open(filename, 'w')
    
    def callback(self, data):
        """
        Write data to file
        """
        if self.file != None:
            t = datetime.datetime.now().time()
            data_str = " ".join(["%02x" % ord(d) for d in data])
            msg = "%s %s\n" % (t.isoformat(), data_str)
            self.file.write(msg)
            self.file.flush()
    
    def close(self):
        """
        Close the file.
        """
        self.file.close()
        self.file = None

