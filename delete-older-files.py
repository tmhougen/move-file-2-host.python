#!/usr/bin/env python3

import sys, getopt, os, time, fnmatch, glob
olderthan = '#days.has.to.be.defined'
path = '#target.directory.has.to.be.defined'
filter = '*'

def usage():
    print('---------------------------------------------------')
    print('Delete files older than...')
    print('---------------------------------------------------')
    print(sys.argv[0], 'needs input args')
    print('-o --olderthan      days, must be defined')
    print('-d --dir            Must / should be defined as a')
    print('                    absolute (/path)')
    print('-f --filter         Dont need, default = "*"')
    print('                    Obs! husk "" eksempel "NO*" ')
    print()
    print('Example:')
    print('  $> ./delete-older-files.py -o365 -d/path -f"*.py"')
    sys.exit('---------------------------------------------------')

def deleteolder(rootpath, filspec, age):
# Set filefilter and for each file, copy to target and remove source.
# os.path.split(path)[1]
    files = fnmatch.filter(os.listdir(rootpath), filspec)
    if len(files) == 0:
        print('No items found: ' + rootpath + " " + filspec)
        return
    now = time.time()
    for filename in files:
        if not os.path.isdir(os.path.join(rootpath, filename)):
            filestamp = os.stat(os.path.join(rootpath, filename)).st_mtime
            filecompare = now - int(age) * 86400
            if  filestamp < filecompare:
                # Put in delete cmd, or make dryrun..
                print("Delete: ", filename)

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

# Run recursive
files = glob.glob(path + '/**', recursive=True)
for name in files:
    if os.path.isdir(name):
        print("Investigate:", name \
        , ", Filter: ", filter \
        , ", Age > ", olderthan)
        deleteolder(name, filter, olderthan)
