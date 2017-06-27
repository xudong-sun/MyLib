import os

from commons import md5sum, generate_files_within_dir

dirs = ['/data/FaceDetection/animals/all_pics']
exts = ('.jpg', '.jpeg', '.png', '.bmp')
#md5_set = set()
md5_map = {}

if __name__ == '__main__':
    for dir_ in dirs:
        assert os.path.isdir(dir_)
        for filename in generate_files_within_dir(dir_, exts):
            md5 = md5sum(filename)
            #if md5 in md5_set: print '! {} identical with some other file'.format(filename)
            #else: md5_set.add(md5)
            if md5 in md5_map: print '! {} vs {}'.format(filename, md5_map[md5])
            else: md5_map[md5] = filename

