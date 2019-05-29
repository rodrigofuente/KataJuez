#!/usr/bin/env python

import sys
import os

def compare(file1, file2):
    bs = 32768 # buffersize, fixed for now
    rb = 0 # read bytes from first file

    if os.stat(file1).st_size != os.stat(file2).st_size: return 1

    with open(file1, 'r') as fd1, open(file2, 'r') as fd2:
        while rb <= os.stat(file1).st_size:
            if fd1.read(bs) != fd2.read(bs):
                return 1
            else:
                rb += bs
        return 0

sys.exit(compare(sys.argv[1], sys.argv[2]))
