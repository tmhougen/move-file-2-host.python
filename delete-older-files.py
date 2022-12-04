#!/usr/bin/env python3

import sys, getopt, os, time
olderthan = '#days.has.to.be.defined'
path = '#target.directory.has.to.be.defined'


def usage():
    print('---------------------------------------------------')
    print('Delete files older than')
    print('---------------------------------------------------')
    print(sys.argv[0], 'needs input args')
    print('-o --olderthan      Must be defined, days')
    print('-d --dir            Must be defined, absolute (/)')
    sys.exit('---------------------------------------------------')

# Block validate input args
argi = sys.argv[1:]
try:
    opts, args = getopt.getopt(argi,"ht:o:d:", \
    ["olderthan=","dir=","help="])
except getopt.GetoptError as err:
    print (err)
    usage()
for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
    elif opt in ("-o", "--olderthan"):
        olderthan = arg
    elif opt in ("-d", "--dir"):
        path = arg
if olderthan == 'path' \
or path == '#target.directory.has.to.be.defined':
    usage()

now = time.time()

for filename in os.listdir(path):
    if not os.path.isdir(os.path.join(path, filename)):
        filestamp = os.stat(os.path.join(path, filename)).st_mtime
        filecompare = now - int(olderthan) * 86400
        if  filestamp < filecompare:
            print(filename)
