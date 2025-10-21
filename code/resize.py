#!/usr/bin/env python3
from PIL import Image
import sys

infile, outfile, width, height = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
im = Image.open(infile)
im.thumbnail((width, height))
im.save(outfile)

