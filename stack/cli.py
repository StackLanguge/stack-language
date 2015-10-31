#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
path = os.path.dirname(os.path.abspath(__file__))  # INSERT PATH HERE

import sys
sys.path.insert(0, path)
import interpeter
if len(sys.argv) != 2:
    sys.exit(0)
filename = sys.argv[1]
try:
    with open(filename) as f:
        prog = f.read()
    print('\n***STARTING PROGRAM***')
    try:
        interpeter.interpet(prog, filename)
    except SystemExit:
        pass
    print('***ENDING PROGRAM***')
except IOError as err:
    print('The file %s does not exist!' % err.filename)
