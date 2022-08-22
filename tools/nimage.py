#! /usr/bin/env python3
# -*- utf-8 -*-

# nimage --- node image processing.
#
# DEPENDS ON:
#    imagemagick (convert)
#    pngquant
#
# Simplify, as best possible, the process of creating node images for
# the documentation. I've found no trivial way. This script is a
# front-end to imagemagick's convert utility that will copy a snapped
# node image to a fixed size in the sphinx-doc's image location.
#
# In Blender,
#   Open Blender and start a geometry node session
#   Shift-a to insert a one or more nodes
#   Enlarge as big as you can
#   Using Window/Save Screenshot(Editor), snap an image of the geometry
#      editor view containing the node
#   Save it to the default ~/Documents/gearbox/screen.png
#
# In GIMP,
#    Open screen.png
#    Set view to 100%
#    Rectangle-select portion containing the node
#    Ctrl-C to select
#    Shift-Ctrl-V to create a new image with the selection
#    Shift-Ctrl-E to Export As ...
#    Name output in lower case, spaces as underscores (_)
#
# In a separate terminal window,
#   Use this utility from the top of the documentation tree,
#   $ ./tools/nimage.py curve_attribute
#   ... presuming this is the "ETK_Curve Attribute" node.
#
# The image will be reduced to 300 pixels wide (and whatever height).
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
                        default='~/Documents/screwbox',
                        help='Source folder of image files.')
    parser.add_argument('--prefix',
                        default='nodes',
                        help='String prepended to the output filename')
    parser.add_argument('--width',
                        default=300,
                        type=int,
                        help='Width in pixels of output image.')
    parser.add_argument('--out-folder',
                        default='./images',
                        help='Output image location.')
    parser.add_argument('--force',
                        action='store_true',
                        help='Overwrite existing file.')
    args = parser.parse_args()
    return args


# Images are processed by piping the output from an imagemagick resize
# into the pngquant utility to compress the filesize.
def main(args):
    imagepath = pathlib.Path(os.path.expanduser(args.in_folder))
    for image in list(imagepath.glob('./*.png')):
        base = '{0}-{1}'.format(
            args.prefix,
            os.path.basename(image).replace('-','_')
        )
        outimage = os.path.join(args.out_folder, base)
        print('Converting {0} -> {1} '.format(image, base))
        convert = ['convert', image]
        if args.width > 0:
            convert.append('-resize')
            convert.append('{0}x'.format(args.width))
        convert.append('-')
        p1 = subprocess.Popen(convert, stdout=subprocess.PIPE)
        quantify = ['pngquant', '--strip', '--quality', '75-95']
        if args.force:
            quantify.append('--force')
        quantify.append('--output')
        quantify.append(outimage)
        quantify.append('-')
        p2 = subprocess.Popen(quantify, stdin=p1.stdout)
        p1.stdout.close()
        p2.communicate()[0]
    return 1


# MAIN
if __name__ == "__main__":
    args = subArgs()
    sys.exit(main(args))
