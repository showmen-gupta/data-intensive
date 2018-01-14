#!/usr/bin/env python
import sys

# Mapper1.py output
# date<TAB>sender<TAB>receivers<TAB>body<TAB>message_id<TAB>message_uri<TAB>count

# Reducer1.py output
# message_uri<TAB>message_id<TAB>date<TAB>sender<TAB>reciever<TAB>body<TAB>id

# file1 = open("m1.txt", 'r')
# for line in file1:

for line in sys.stdin:
    parts = line.split("\t")
    iid = parts[-1]
    recievers = parts[2].split(',')

    for r in recievers:
        print "\t".join([parts[5], parts[4], parts[0], parts[1], r, parts[3]])
