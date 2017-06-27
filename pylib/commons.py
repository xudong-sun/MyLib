'''
common python utilities
'''

def assure_dir(dir_):
    '''make sure dir_ exists'''
    if not dir_: return
    import os
    if not os.path.exists(dir_): os.makedirs(dir_)

def check_file_exists(file_):
    '''assert file_ exists'''
    import os.path as osp
    assert osp.exists(file_), 'check failed: {} not exists'.format(file_)

def check_file_extension(file_, valid_extensions):
    '''check whether the extension of file_ is in valid_extensions'''
    import os
    ext = os.path.splitext(file_)[1]
    for valid_ext in valid_extensions:
        if ext.lower() == valid_ext.lower(): return True
    return False

def remove_file(file_):
    '''remove a file if it exists'''
    import os
    if os.path.exists(file_): os.remove(file_)

def pickle_to_file(object_, file_):
    '''pickle object_ to file_'''
    import cPickle
    with open(file_, 'wb') as fout: cPickle.dump(object_, fout)

def pickle_from_file(file_):
    '''load object from file_. returns the object'''
    import cPickle
    with open(file_, 'rb') as fin: object_ = cPickle.load(fin)
    return object_

def generate_files_within_dir(root_dir, exts=None, FILTER="True"):
    '''generator to yield all files with extension in exts, and filtered by FILTER
    exts: a collection of extensions, if None, any extension will be valid
    FILTER: additional filter
    '''
    import os
    for cur_dir, dirs, files in os.walk(root_dir):
        for file_ in files:
            if (exts is None or check_file_extension(file_, exts)) and eval(FILTER):
                yield os.path.join(cur_dir, file_)

def md5sum(file_):
    '''calculate md5 of a given file, return str in hex
    '''
    import os.path as osp
    import hashlib
    assert osp.isfile(file_), 'md5sum error: {} not accessible or is not a file'.format(file_)
    with open(file_) as f: return hashlib.md5(f.read()).hexdigest()

def wait_for_key_input(valid_keys=['']):
    '''wait for user typing a specific set of keys
    valid_keys: list[str]
    returns: user-typed key
    '''
    while True:
        key = raw_input()
        if key in valid_keys: break
        else: print 'Valid keys are', valid_keys
    return key

def get_logger():
    '''return a logger registered with a StreamHandler
    '''
    import logging
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    return logger

