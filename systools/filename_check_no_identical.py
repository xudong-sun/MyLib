import os

from commons import generate_files_within_dir

dirs = ['/data/FaceDetection/animals/all_pics']
exts = ('.jpg', '.jpeg', '.png', '.bmp')
filename_map = {}

if __name__ == '__main__':
    for dir_ in dirs:
        assert os.path.isdir(dir_)
        for filename in generate_files_within_dir(dir_, exts):
            name = os.path.basename(filename)
            if name in filename_map: print '! {} vs {}'.format(filename, filename_map[name])
            else: filename_map[name] = filename

