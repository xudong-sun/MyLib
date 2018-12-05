'''
common python utilities
'''

def assure_dir(dir_):
    '''make sure dir_ exists'''
    if not dir_: return
    import os
    assert not os.path.isfile(dir_), '{} is a file'.format(dir_)
    if not os.path.isdir(dir_): os.makedirs(dir_)

def check_file_exists(file_):
    '''assert file_ exists
    file_ can be either a file or a directory
    '''
    import os.path as osp
    assert osp.exists(file_), 'check failed: {} not exists'.format(file_)

def check_file_extension(file_, valid_extensions):
    '''check whether the extension of file_ is in valid_extensions
    extensions are case-insensitive
    '''
    import os
    ext = os.path.splitext(file_)[1]
    for valid_ext in valid_extensions:
        if ext.lower() == valid_ext.lower(): return True
    return False

def remove_file(file_):
    '''remove a file if it exists'''
    import os
    if os.path.isfile(file_): os.remove(file_)

def remove_dir(dir_):
    '''remove a directory if it exists'''
    import os
    if os.path.isdir(dir_): os.removedirs(dir_)

def pickle_to_file(object_, file_):
    '''pickle object_ to file_'''
    import cPickle
    import os
    assure_dir(os.path.dirname(file_))
    with open(file_, 'wb') as fout: cPickle.dump(object_, fout)

def pickle_from_file(file_):
    '''load object from file_. returns the object'''
    import cPickle
    with open(file_, 'rb') as fin: object_ = cPickle.load(fin)
    return object_

def generate_files_within_dir(root_dir, exts=None, FILTER="True", followlinks=True):
    '''generator to yield all files with extension in exts, and filtered by FILTER
    exts: a collection of extensions, if None, any extension will be valid
    FILTER: additional filter
    followlinks: whether to follow symbolic links
    '''
    import os
    for cur_dir, dirs, files in os.walk(root_dir, followlinks=followlinks):
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

def get_git_hash():
    '''get git hash of current git commit
    '''
    import subprocess
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()

def get_timestamp():
    '''get current timestamp in string format
    '''
    from datetime import datetime
    return datetime.now().strftime('%Y_%m_%d_%H:%M:%S')

def wait_for_key_input(valid_keys=['']):
    '''wait for user typing a specific set of keys
    valid_keys: list[str]
    returns: user-typed key
    '''
    while True:
        key = raw_input()
        if key in valid_keys: break
        else: print('Valid keys are ' + str(valid_keys))
    return key

def simple_logger():
    '''return a simple logger registered with a StreamHandler
    '''
    import logging
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    return logger

class Timer(object):
    '''A simple timer for calculating average speed
    '''
    global time
    import time
    def __init__(self):
        self.reset()
    def tic(self):
        self.start = time.time()
    def toc(self):
        self.time += time.time() - self.start
        self.count += 1
    def get(self):
        return self.time / self.count
    def reset(self):
        self.time = 0
        self.count = 0

def no_args_decorator(f):
    """ A decorator for decorators
    This decorator allows the decorated decorator used both in the form of @decorator(arguments) and @decorator.
    In the second case, the default arguments will be applied.
    The only restriction is that, the decorator cannot take a single callable as its arguments.
    """
    def g(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return f()(args[0])  # second case
        else:
            return f(*args, **kwargs)  # first case
    return g

@no_args_decorator
def timeit(freq=1, rep=1):
    """ Decorator for calculating average runtime
    freq: int, print average runtime after every `freq` calls to the original function
          if freq=0, will never print automatically, but you can always call func.avg_time to check average runtime
    rep: int, repeatedly call func `rep` times to calculate the average runtime. If rep > 1, this will override freq and set freq = rep
    """
    import time
    if rep > 1: freq = rep
    class decorator(object):
        def __init__(self, func):
            self.func = func
            self.__name__ = func.__name__
            self.total = 0.
            self.count = 0
        def __call__(self, *args, **kwargs):
            start = time.time()
            for _ in range(rep):
                rv = self.func(*args, **kwargs)
            self.total += time.time() - start
            self.count += rep
            if freq > 0 and self.count % freq == 0:
                print("Called {}() {} times, average runtime = {} s".format(self.__name__, self.count, self.avg_time))
            return rv
        @property
        def avg_time(self):
            return self.total / self.count
    return decorator

