#!/usr/bin/env python
# encoding: utf-8
"""
dump2csv.py

Created by Oliver Smith on 2010-01-17.
Copyright (c) 2010 Oliver Smith. All rights reserved.
"""

import sys

from subaru import SELECT_MONITOR_FIELDS

header_printed = False

def translate(line):
    global header_printed
    fields = line.split()
    timestamp = fields[0]
    first,last = [int(i) for i in fields[1].strip('[]').split('-')]
    data = [int(i,16) for i in fields[2:]]
    if header_printed == False:
        headers = []
        for i in range(first, last+1):
            if i in SELECT_MONITOR_FIELDS:
                headers.append('"%s (%s)"' % (SELECT_MONITOR_FIELDS[i][0],
                                              SELECT_MONITOR_FIELDS[i][1]))
        print ','.join(headers)
        header_printed = True
    fmtd_data = []
    for d in range(len(data)):
        if (d+first) in SELECT_MONITOR_FIELDS:
                fmtd_data.append(str(SELECT_MONITOR_FIELDS[d+first][2](data[d])))
    print ','.join(fmtd_data)


def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            for l in f.readlines():
                translate(l)
    else:
        print "Syntax: dump2csv.py FILENAME"


if __name__ == '__main__':
    main()

