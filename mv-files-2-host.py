#!/usr/bin/env python3
# TODO: Maybe make multiple target-hosts, the first one has priority
# Nededs public ssh key installed on target

# Defaults
src_dir = './'
src_filter = '*'
trg = "#target.host.has.to.be.defined"
trg_dir = '#target.directory.has.to.be.defined'
maxlogfilesize = 10240

import sys, getopt
import os, fnmatch
from subprocess import PIPE, Popen
from datetime import datetime
from contextlib import suppress
from pathlib import Path

def usage():
    print('---------------------------------------------------')
    print('Moves files from this host to other host using scp')
    print('You must have public key configured om targethost')
    print('---------------------------------------------------')
    print(sys.argv[0], 'needs input args')
    print('-t --targethost     Must be defined.')
    print('                    (usr@)hostname or hostname ')
    print('-d --targetdir      Must be defined')
    print('                    relative:targetpath')
    print('                    absolute:/targetpath')
    print('-f --sourcefilter   Dont need, default = "*"')
    print('                    Obs! husk "" eksempel "NO*" ')
    print('-s --sourcedir      Dont need, default = current')
    sys.exit(1)

def rotatelogs(maxfilesize):
    lname = sys.argv[0] + '.logs/moved-files'
    fromname = f'{lname}{0}'
    os.makedirs(os.path.dirname(fromname), exist_ok=True)
    Path(fromname).touch()
    if os.path.getsize(lname + '0') >= maxlogfilesize:
        Path(lname + '6').touch()
        os.remove(lname + '6')
        for x in range(6, 0, -1):
            fromname = f'{lname}{x - 1}'
            toname = f'{lname}{x}'
            Path(fromname).touch()
            os.rename(fromname, toname)
    return fromname

def verifyTarget(targethost, targethostdir):
    command = ['ssh', targethost, 'cd', targethostdir]
    process = Popen(command, stderr=PIPE, stdout=PIPE)
    stdout, stderr = process.communicate()
    exit_code = process.wait()
    if exit_code != 0:
        print('[ERR] cant locate ' + trg_dir + ' on ' + trg)
        print (stderr)
        print('-------------------------------------------------')
        print(' - Tips: ssh ' + trg + ' \"mkdir ' + trg_dir + '\"')
        print(' - Tips: ssh-copy-id ' + trg)
        return 1
    return 0


# Block validate input args
argi = sys.argv[1:]
try:
    opts, args = getopt.getopt(argi,"ht:d:f:s:h:", \
    ["targethost=","targetdir=","sourcefilter=","sourcedir=","help="])
except getopt.GetoptError as err:
    print (err)
    usage()
for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
    elif opt in ("-f", "--sourcefilter"):
        src_filter = arg
    elif opt in ("-s", "--sourcedir"):
        src_dir = arg
    elif opt in ("-t", "--targethost"):
        trg = arg
    elif opt in ("-d", "--targetdir"):
        trg_dir = arg
if trg == '#target.host.has.to.be.defined' \
or trg_dir == '#target.directory.has.to.be.defined':
    usage()

# Check if target dir exists
print(verifyTarget(trg, trg_dir))
# Block, move files from sourcedir to tatget useing scp for copy and ssh to delete


# Set filefilter and for each file, copy to target and remove source.
files = fnmatch.filter(os.listdir(src_dir), src_filter)
if len(files) == 0:
    sys.exit('No files found in ' + src_dir + src_filter)
for fname in files:
    if not os.path.isdir(os.path.join(src_dir, fname)):
        # print(fname)
        workfname = '.' + fname
        date_string = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
        os.rename(os.path.join(src_dir,fname), os.path.join(src_dir,workfname))

        copyCmd = 'scp -q ' + os.path.join(src_dir,workfname) + ' ' \
        + trg + ':' + trg_dir + '/' + workfname

        setOrginalNamecmd = 'ssh ' + trg + ' "mv ' +  trg_dir \
        + '/' + workfname + ' ' + trg_dir + '/' + fname  + '"'

        if os.system(copyCmd) == 0:
            if os.system(setOrginalNamecmd) == 0:
                if os.access(os.path.join(src_dir,workfname), os.W_OK):
                    with suppress(OSError):
                        os.remove(os.path.join(src_dir,workfname))
                else:
                    print('Could not remove: ' + fname)
        else:
            sys.exit('[ERR] Could not copy to ' + trg + ':' + trg_dir + '/.' + fname)

        logfilename = rotatelogs(maxlogfilesize)
        with open(logfilename , "a") as f:
            f.write(date_string + " " +trg + ':' \
            + trg_dir + '/' + fname + '\n')

sys.exit(0)
