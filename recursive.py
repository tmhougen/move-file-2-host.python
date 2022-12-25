#!/usr/bin/env python3


import os, glob

my_path=input("Enter your path -: ")
files = glob.glob(my_path + '/**', recursive=True)
for name in files:
    if os.path.isdir(name):
        print(name)
