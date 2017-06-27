#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -------------------------------
# Fix the newline character in different os
#
# Usage: python fix_newline.py YOUR_FILE [--backup]
# If --backup flag is set, the original file will be copied as a .bak file
#
# Created by Xudong Sun, 2016-08-29
# -------------------------------

import sys, os
import argparse

from commons import remove_file, wait_for_key_input

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='file to be converted')
    parser.add_argument('--backup', help='backup original file', action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    filename = args.file
    backup_name = filename + '.bak'
    os.rename(filename, backup_name)
    with open(backup_name) as fin:
        with open(filename, 'w') as fout:
            for line in fin: print>>fout, line.strip()
    print '>> File has been converted. Please check, then enter "done" or "abort"'
    key = wait_for_key_input(['done', 'abort'])
    if key == 'done':
        if not args.backup: remove_file(backup_name)
        print 'Conversion succeeded'
    else:
        remove_file(filename)
        os.rename(backup_name, filename)
        print 'Original file has been recovered'

