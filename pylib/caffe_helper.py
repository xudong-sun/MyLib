# coding: utf-8
# --------------------------------
# class for grouping input data and generating minibatch
# written by Xudong
# --------------------------------

import random
import numpy as np

EPISILON = 1e-4

class MinibatchGenerator(object):
    def __init__(self, probs, batch_size):
        '''probs: a list of probs that add up to 1, probability of each group that may appear in a minibatch
        batch_size: number of data to be return when calling get_next_minibatch()
        '''
        assert abs(sum(probs) - 1) < EPISILON, 'sum of probs is not 1'
        self.group_count = len(probs)
        self.probs = probs
        self.data = []
        for i in xrange(self.group_count): self.data.append([])
        self._batch_size = batch_size
        self._ready = False  # must be True on calling _get_next_minibatch

    def add_data(self, data, group_idx):
        '''add data to a specific group
        data can be of any type
        group_idx start from 0
        '''
        self.data[group_idx].append(data)

    def ready(self):
        '''initialize current_idx for training'''
        self.data_idx = [np.arange(len(self.data[i])) for i in xrange(self.group_count)]  # idx pointing to self.data
        self.current_idx = [len(self.data[i]) - 1 for i in xrange(self.group_count)]      # idx pointing to self.data_idx
        print 'Total number of data:', [len(data) for data in self.data]
        self._ready = True

    def _shuffle_data(self, group_idx):
        random.shuffle(self.data_idx[group_idx])

    def get_next_minibatch(self):
        '''return a minibatch with size self._batch_size, data from each group appear according to their probabilities
        You must call ready() before calling this method
        '''
        assert self._ready, 'You must call MinibatchGenerator.ready() before calling get_next_minibatch()'
        data = []
        for i in xrange(self._batch_size):
            group_idx = self._random_group()
            self.current_idx[group_idx] += 1
            if self.current_idx[group_idx] == len(self.data[group_idx]):
                self._shuffle_data(group_idx)
                self.current_idx[group_idx] = 0
            idx = self.data_idx[group_idx][self.current_idx[group_idx]]
            data.append(self.data[group_idx][idx])
        return data

    def _random_group(self):
        '''select a random group according to self.probs'''
        p = random.random()
        for group_idx in xrange(self.group_count):
            if p < self.probs[group_idx]: return group_idx
            else: p -= self.probs[group_idx]
        return group_idx - 1
