# coding=utf-8

# ---------------------------------
# Lists all files whose last modified time is later than a given timestamp
# Created by Xudong, 2016-09-29
#
# Usage: python list_modified_files.py root_dir timestamp [--exclude_exts EXCLUDE_EXTS]
#
# timestamp:    in the format %Y-%m-%d-%H-%M-%S or %Y-%m-%d
#               files whose modified time later than this timestamp will be displayed
# exclude_exts: a list of extensions separated by comma
#               files with those extensions will NOT be displayed
#
# Example: python list_modified_files.py /root/dir 2016-09-29-12-00-00 --exclude_exts swp,tmp
# ---------------------------------

import sys, os, time, re, argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('root_dir', help='root dir')
    parser.add_argument('timestamp', help='list modified files after "timestamp"')
    parser.add_argument('--exclude_exts', help='excluded extensions', default=None)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    directory = args.root_dir
    timestamp = args.timestamp
    exclude_exts = [] if args.exclude_exts is None else args.exclude_exts.split(',')
    
    PRINT_TIME = lambda timestamp: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    
    timestamp_ = re.sub('\D', '-', timestamp)
    try:
        timestamp = time.strptime(timestamp_, '%Y-%m-%d-%H-%M-%S')
    except ValueError:
        try:
            timestamp = time.strptime(timestamp_, '%Y-%m-%d')
        except ValueError:
            print 'Unable to parse time: ', timestamp
            sys.exit(-1)
    timestamp = time.mktime(timestamp)
    print '>> Listing all files that were modified later than', PRINT_TIME(timestamp)
    if len(exclude_exts) > 0: print '>> Exclude files with the following extensions:', ', '.join(exclude_exts)
    
    count = 0
    for curDir, dirs, files in os.walk(directory):
        for file_ in files:
            if os.path.splitext(file_)[1][1:] in exclude_exts: continue
            filename = os.path.join(curDir, file_)
            mtime = os.path.getmtime(filename)
            if mtime > timestamp:
                print PRINT_TIME(mtime), filename
                count += 1
    print '>>', count, 'files found'
    
