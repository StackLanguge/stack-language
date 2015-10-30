import sys
import interpeter
import os
print('***Stack 2.0 Program Runner***')
print("Running on Python", sys.version.split()[0])
while True:
    filename = input('Enter file name (nothing to exit): ')
    if not filename:
        break
    try:
        cd = os.path.abspath(os.path.dirname(filename))
        print(cd)
        os.chdir(cd)
        with open(os.path.basename(filename)) as f:
            prog = f.read()
        print('\n***STARTING PROGRAM***')
        try:
            interpeter.interpet(prog)
        except SystemExit:
            pass
        print('***ENDING PROGRAM***')
    except IOError:
        print('The file %s does not exist!' % filename)
