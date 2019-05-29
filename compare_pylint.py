#!/usr/bin/env python

import sys
import os

if __name__ == '__main__':
    BUFFER_SIZE = 32768
    READ_BYTES = 0
    FILE1 = sys.argv[1]
    FILE2 = sys.argv[2]

    if len(sys.argv) != 3:
        exit(1)

    if os.stat(FILE1).st_size != os.stat(FILE2).st_size:
        exit(1)

    with open(FILE1, 'r+b') as fd1, open(FILE2, 'r+b') as fd2:
        while READ_BYTES <= os.stat(FILE1).st_size:
            if fd1.read(BUFFER_SIZE) != fd2.read(BUFFER_SIZE):
                exit(1)
            READ_BYTES += BUFFER_SIZE
