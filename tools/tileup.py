#! /usr/bin/env python3
# -*- utf-8 -*-
#
# This script is a front-end for an imagemagick montage commmand that
# will compose any images ending in "-n.png" into a horizontally tiled
# image containing those images. The command looks in a particular
# folder for this and generates the montage in an output file named
# with the common prefix of all the files + "-comp.png".
#
# The default input folder is $HOME/Documents/etk which can be changed
# on the command line. The output will be in the same folder (it does
# not process it like nimage.py does.)
#
# IMPORTANT: It is presumed (!) that this is being used for horizontal
# example images and they are processed in this order:
#   Create example-foo-1.png
#   Create example-foo-2.png
#   Create example-foo-3.png
#   ... or more
#   Run tileup.py to create example-foo-comp.png
#   Move the individual images out of the way so they don't get mung'd
#   with nimage,
#      mv example-foo-?.png ./src
#   run nimage.py --width 800
#

import argparse
import os
import os.path
import pathlib
import subprocess
import sys

def subArgs():
    parser = argparse.ArgumentParser(description='nimage args parsing')
    parser.add_argument('--in-folder',
                        default='~/Documents/etk',
                        help='Source folder of image files.')
    args = parser.parse_args()
    return args


def main(args):
    imagepath = pathlib.Path(os.path.expanduser(args.in_folder))
    ilist = []
    for image in sorted(imagepath.glob('./*-[0-9].png')):
        ilist.append(image)
    if len(ilist) < 1:
        print('No images found to tile')
    elif len(ilist) < 2 :
        print('Only one image?')
    else:
        montage = ['montage',
                   '-border',
                   '0',
                   '-mode',
                   'concatenate',
                   '-tile',
                   '{0}x1'.format(len(ilist)),
                   ]
        for image in ilist:
            montage.append(os.fspath(image))
        outpath = os.path.commonprefix(ilist) + 'comp.png'
        montage.append(outpath)
        print('Creating tiled montage: {0}'.format(outpath))
        subprocess.run(montage)
        return 0
    return -1


# MAIN
if __name__ == "__main__":
    args = subArgs()
    sys.exit(main(args))
