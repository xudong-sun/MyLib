import mxnet as mx
import numpy as np
import os
import time
from multiprocessing import Process, Queue

from commons import pickle_from_file

class BaseLoader(mx.io.DataIter):
    """
    Base data loader for MXNet training
    """
    def __init__(self, root='', batch_size=16, split='train', shuffle=False, include_trailing=False, num_workers=4, prefetch_ratio=3.0, cached_dataset=''):
        """
        shuffle: whether to shuffle the dataset in each epoch
        include_trailing: when num_workers == 1, this determines whether to include the final few samples. Useful for validation.
        num_workers: number of worker processes to read data. Multiple workers mode is only supported in training phase.
        prefetch_ratio: this determines the size of the prefetch queue in terms of batch_size
        cached_dataset: if specified, will use the cached dataset instead of reading from disk. The cached dataset is a list of (data, label). If cached_dataset is specified, this will override include_trailing, num_workers, prefetch_ratio.
        To extend this base loader, implement _set_input_shapes(), 
        """
        self.root = root
        self.batch_size = batch_size
        self.split = split

        # shuffle dataset before each epoch begins
        self.shuffle = shuffle
        if self.split == 'train' and self.shuffle == False:
            print "Warning: Phase is set to train, but shuffle flag is False."
        elif self.split != 'train' and self.shuffle == True:
            print "Warning: Phase is set to {}, but shuffle flag is True.".format(self.split)

        # whether to include the trailing batch with less than batch_size samples
        # if True, the last batch will be padded by the last sample to make batch_size the same
        self.include_trailing = include_trailing
        if self.split == 'train' and self.include_trailing == True:
            print "Warning: Phase is set to train, but include_trailing flag is True."
        elif self.split != 'train' and self.include_trailing == False:
            print "Warning: Phase is set to {}, but include_trailing flag is False.".format(self.split)

        self.num_workers = num_workers
        self.prefetch_ratio = prefetch_ratio
        if self.split != 'train' and self.num_workers > 1:
            print "Warning: multiple workers mode is not fully supported in validation/test mode."

        # dataset. May use a cached dataset to avoid any randomness
        self.cached_dataset = cached_dataset
        if self.cached_dataset == '':
            print 'Reading dataset from', self.root
            self._read_dataset()
        else:
            print 'Reading cached dataset from', self.cached_dataset
            self._read_cached_dataset()
        self.num_samples = len(self.dataset)
        print 'Number of samples:', self.num_samples

        # calculate number of batches
        self.num_batches = self.num_samples // self.batch_size
        if self.include_trailing and self.num_batches * self.batch_size < self.num_samples:
            self.num_batches += 1  # final batch
            self.trailing_count = self.num_samples - self.num_batches * self.batch_size

        # specify input shapes
        self._set_input_shapes()
        print 'data_shape:', self.data_shape, 'label_shape:', self.label_shape

        self.reset()

    def _set_input_shapes(self):
        """
        specify self.data_shape, self.label_shape
        """
        raise NotImplementedError

    def start_workers(self):
        """ split dataset into num_workers parts, spawn a process to read from each part """
        if self.num_workers > 1:
            self.data_queue = Queue()
            ids = list(np.linspace(0, self.num_samples, self.num_workers, endpoint=False, dtype=int))
            ids.append(self.num_samples)
            for i in xrange(self.num_workers):
                p = Process(target=self._data_worker, args=(np.arange(ids[i], ids[i+1]),))
                p.daemon = True
                p.start()

    def _data_worker(self, worker_ids):
        """ code for each worker process
        workers_ids: indices for self.dataset. Subset of all indices for this worker process
        """
        ids = np.arange(len(worker_ids))
        if self.shuffle: np.random.shuffle(ids)
        ids_ptr = 0
        while True:
            if self.data_queue.qsize() > self.batch_size * self.prefetch_ratio: # enough data in data_queue
                time.sleep(1)
            else:
                if ids_ptr == len(worker_ids):
                    ids_ptr = 0
                    if self.shuffle: np.random.shuffle(ids)
                idx = worker_ids[ids[ids_ptr]]
                data, label = self._get_item(idx)
                self.data_queue.put((data, label))
                ids_ptr += 1

    def reset(self):
        self.batch_idx = 0
        if self.num_workers == 1:
            self.ids = np.arange(self.num_samples)
            if self.shuffle:
                np.random.shuffle(self.ids)

    def _read_dataset(self):
        raise NotImplementedError

    def _read_cached_dataset(self):
        self.dataset = utils.pickle_from_file(self.cached_dataset)

    @property
    def provide_data(self):
        return [('data', self.data_shape)]

    @property
    def provide_label(self):
        return [('label', self.label_shape)]

    def next(self):
        if self._has_next_batch():
            return self._next_batch()
        else:
            raise StopIteration

    def _get_item(self, index):
        """ get inputs without using cache
        index: index for self.dataset
        returns: a tuple of (data, label), with shapes specified as self.data_shape, self.label_shape
        """
        raise NotImplementedError

    def _has_next_batch(self):
        return self.batch_idx < self.num_batches

    def __len__(self):
        return self.num_batches

    def __getitem__(self, i):
        if self.cached_dataset == '':
            data, label = self._get_item(i)
        else:
            data, label = self.dataset[i]
        return data, label

    def _next_batch(self):
        start_idx = self.batch_idx * self.batch_size
        self.batch_idx += 1
        batch_data = np.zeros(self.data_shape)
        batch_label = np.zeros(self.label_shape, dtype=np.int32)
        for i in xrange(self.batch_size):
            if self.num_workers == 1:
                data, label = self.__getitem__(self.ids[min(i+start_idx, self.ids.size-1)])
            else:
                data, label = self.data_queue.get()
            batch_data[i] = data
            batch_label[i] = label
        batch_data = [mx.nd.array(batch_data)]
        batch_label = [mx.nd.array(batch_label)]
        return mx.io.DataBatch(data=batch_data, label=batch_label)


###################################
# some dataset utilities
###################################

def cache_dataset(dataloader, output):
    """ Cache the dataset. The cached pkl file can be passed to `cached_dataset` """
    from commons import pickle_to_file
    data = []
    for i, batch in enumerate(dataloader):
        batch_data = batch.data[0].asnumpy()
        batch_label = batch.label[0].asnumpy()
        end = (i+1) * dataloader.batch_size
        if end > dataloader.num_samples:
            batch_data = batch_data[:dataloader.trailing_count]
            batch_label = batch_label[:dataloader.trailing_count]
        for j in xrange(batch_label.shape[0]):
            data.append((batch_data[j], batch_label[j]))
    pickle_to_file(data, output)


