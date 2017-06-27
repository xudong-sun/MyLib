'''
simple algorithms
'''

def kmeans(data, k, distance=None, initial_centeroids=None, iteration_threshold=1e-4, max_iteration=1000, stop_at_local_minimum=False, verbose=False):
    '''k-means algorithm
    data: N*D ndarray, i.e. N D-dimensional vectors
    distance function defaults to Euclidean. For user-specified distance function, the format is dist = distance(x1, x2), see Euclidean function
    initial_centeroids are randomly selected from data, if not given
    iteration_threshold: converge if difference of two iterations is below this value
    max_iteration: stop iteration if number of iterations exceeds this value
    verbose: if this flag is set, print out iteration details
    returns: centeroids, group_ids
    centeroids: k*D ndarray
    group_ids: vector of size N, i-th entry is an index [0, k), specifying which the group index it belongs to
    '''
    import numpy as np

    def Euclidean(x1, x2):
        '''exemplar (Euclidean) distance function
        x1 and x2 are both 1d ndarray, return Euclidean distance'''
        diff = x1 - x2
        return np.sum(np.multiply(diff, diff))

    def update_group_index(data, centeroids):
        group_ids = np.zeros(data_size)
        total_diff = 0
        for i in xrange(data_size):
            min_diff = 0x7fffffff
            idx = -1
            for j in xrange(k):
                diff = distance(data[i, :], centeroids[j, :])
                if diff < min_diff:
                    min_diff = diff
                    idx = j
            group_ids[i] = idx
            total_diff += min_diff
        return group_ids, total_diff
    
    def update_centeroids(data, centeroids, group_ids):
        for i in xrange(k):
            ids = np.where(group_ids == i)[0]
            if ids.size > 0:
                data_ = data[ids, :]
                centeroids[i, :] = np.sum(data_, 0) / ids.size
            else:
                if verbose: print 'No data points around centeroid', i, 'Re-initializing...'
                centeroids[i, :] = data[np.random.randint(0, data_size, 1), :]

    data_size = data.shape[0]
    if distance is None: distance = Euclidean
    if initial_centeroids is None:
        ids = np.random.randint(0, data_size, k)
        centeroids = data[ids, :]
    else:
        centeroids = initial_centeroids
    
    prev_diff = 0x7fffffff
    diff = prev_diff / 2
    iter_ = 0
    while abs(diff - prev_diff) > iteration_threshold and iter_ < max_iteration:
        iter_ += 1
        prev_diff = diff
        group_ids, diff = update_group_index(data, centeroids)
        if verbose: print 'iteration', iter_, 'loss = ', diff
        if stop_at_local_minimum and diff > prev_diff: break
        update_centeroids(data, centeroids, group_ids)
    
    return centeroids, group_ids


def _kmeans_demo():
    import numpy as np
    import matplotlib.pyplot as plt
    data = np.random.random((1000, 2))
    k = 4
    color = 'rgbc'
    centeroids, group_ids = kmeans(data, k, verbose=True)
    for i in xrange(k):
        ids = np.where(group_ids == i)[0]
        x = data[ids, :]
        plt.plot(x[:,0], x[:,1], color[i] + '.', markersize=5)
        plt.plot(centeroids[i,0], centeroids[i,1], color[i] + 'o', markersize=10)
    plt.show()

if __name__ == '__main__':
    _kmeans_demo()

