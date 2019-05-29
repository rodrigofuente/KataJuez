#!/usr/bin/env python

import sys
import os
import mmap
from multiprocessing import Process, Queue
import xxhash


def calculate_hash(file_desc, queue):
    file_map = mmap.mmap(file_desc.fileno(), 0)
    queue.put(xxhash.xxh64(file_map).digest())


if __name__ == '__main__':
    FILE1 = sys.argv[1]
    FILE2 = sys.argv[2]

    if len(sys.argv) != 3:
        exit(1)

    if os.stat(FILE1).st_size != os.stat(FILE2).st_size:
        exit(1)

    with open(FILE1, 'r+b') as file_desc1, open(FILE2, 'r+b') as file_desc2:
        QUEUE = Queue()
        PROC1 = Process(target=calculate_hash, args=(file_desc1, QUEUE))
        PROC2 = Process(target=calculate_hash, args=(file_desc2, QUEUE))

        PROC1.start()
        PROC2.start()

        RESULTS = []
        for i in 0, 1:
            RESULTS.append(QUEUE.get())

        PROC1.join()
        PROC2.join()

        if RESULTS[0] != RESULTS[1]:
            exit(1)
