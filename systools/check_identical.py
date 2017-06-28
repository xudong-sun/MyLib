#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------------
# This script checks whether any two files are identical or have identical names.
# Created by Xudong, 2017-03-28
#
# Usage: python check_identical.py [TASK] [DIRS] --exts [EXTENSIONS]
#
# TASK:        a string specifying the item to check
#              this is either "md5" (to check whether two files are identical) or "filename" (to check whether two files have identical names)
# DIRS:        a list of root directories to check. Multiple directories should be separated by spaces
# EXTENSIONS:  a list of file extensions to check
#              only files with the given extensions will be checked. Multiple extensions should be separated by spaces
#              if None (default), or omitted, all files will be checked
#
# Example: python check_identical.py filename /data/dir1 /data/dir2 --ext jpg jpeg png bmp
# --------------------------------------

import os
import argparse

from commons import generate_files_within_dir, md5sum

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('task', help='task type, either md5 or filename', choices=['md5', 'filename'])
    parser.add_argument('root_dirs', nargs='+', help='root directories')
    parser.add_argument('--exts', nargs='+', help='extensions to check [None]', default=None)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print args
    mapping = {}  # mapping from key (md5 or basename) to abspath
    for dir_ in args.root_dirs:
        assert os.path.isdir(dir_)
        for filename in generate_files_within_dir(dir_, ['.'+e for e in args.exts]):
            if args.task == 'filename': key = os.path.basename(filename)
            elif args.task == 'md5': key = md5sum(filename)
            if key in mapping: print '! {} vs {}'.format(filename, mapping[key])
            else: mapping[key] = filename

