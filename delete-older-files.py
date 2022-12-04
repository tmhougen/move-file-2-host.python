#!/usr/bin/env python3

import sys, getopt, os, time, fnmatch
olderthan = '#days.has.to.be.defined'
path = '#target.directory.has.to.be.defined'
filter = '*'

def usage():
    print('---------------------------------------------------')
    print('Delete files older than...')
    print('---------------------------------------------------')
    print(sys.argv[0], 'needs input args')
    print('-o --olderthan      days, must be defined')
    print('-d --dir            Must be defined absolute (/path)')
    print('-f --filter         Dont need, default = "*"')
    print('                    Obs! husk "" eksempel "NO*" ')
    sys.exit('---------------------------------------------------')

# Block validate input args
argi = sys.argv[1:]
try:
    opts, args = getopt.getopt(argi,"ht:o:d:f:", \
    ["olderthan=","dir=","filter=","help="])
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
    elif opt in ("-f", "--filter"):
        filter = arg
if olderthan == 'path' \
or path == '#target.directory.has.to.be.defined':
    usage()

# Set filefilter and for each file, copy to target and remove source.
files = fnmatch.filter(os.listdir(path), filter)
if len(files) == 0:
    sys.exit('No files found in ' + path + filter)
now = time.time()
for filename in files:
    if not os.path.isdir(os.path.join(path, filename)):
        filestamp = os.stat(os.path.join(path, filename)).st_mtime
        filecompare = now - int(olderthan) * 86400
        if  filestamp < filecompare:
            print(filename)
