#!/usr/bin/env python
# -*- coding: utf-8 -*-

# batch rename all images in a given directory

import os
import sys
from commons import generate_files_within_dir

IMAGE_FILTER = ('.jpg', '.jpeg', '.png', '.bmp')

if __name__ == '__main__':
    root_dir = sys.argv[1]
    for idx, filename in enumerate(generate_files_within_dir(root_dir, IMAGE_FILTER)):
        newname = os.path.join(os.path.dirname(filename), str(idx) + os.path.splitext(filename)[1])
        os.rename(filename, newname)

