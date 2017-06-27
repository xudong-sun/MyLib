# coding=utf-8

import sys

old_filename = sys.argv[1]
new_filename = old_filename
old_filename += '.bak'
with open(old_filename) as f:
    with open('new_filename', 'wt') as fout:
        for line in f:
            fout.write(line.strip()+'\n')

