#########################################
# plot point cloud with mayavi.mlab
#########################################

import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab

def _plot_color(data, label, scale_factor, color={}):
    if color == {}:
        color = {0: (0,1,1), 1: (1,0,0), 2: (1,1,0), 3: (0,1,0)}
    all_label = np.unique(label)
    for l in all_label:
        x = data[label == l]
        c = color.get(l)
        if c is None:
            c = tuple(np.random.random(3))
        mlab.points3d(x[:,0], x[:,1], x[:,2], color=c, scale_factor=scale_factor)

def plot(data, subsample=None, size=1, title=''):
    """
    data: Nx3 numpy array
    subsample: number of subsampled input point cloud
    """
    if subsample is not None:
        ids = np.random.choice(data.shape[0], subsample, replace=False)
        data = data[ids]
    mlab.points3d(data[:,0], data[:,1], data[:,2], scale_factor=0.01*size)
    if title:
        mlab.title(title)
    mlab.show()

def plot_with_labels(data, label, subsample=None, size=1, color={}, title=''):
    """
    data: Nx3 numpy array
    label: N, numpy array
    subsample: number of subsampled input point cloud
    size: size of points
    color: dict int->tuple(3)
    """
    if subsample is not None:
        ids = np.random.choice(data.shape[0], subsample, replace=False)
        data = data[ids]
        label = label[ids]
    _plot_color(data, label, 0.01*size, color=color)
    if title:
        mlab.title(title)
    mlab.show()

def plot_with_cmap(data, color, num_bins=50, subsample=None, size=1, title=''):
    """
    data: Nx3 numpy array
    color: N, numpy array
    num_bins: int, discretize color into num_bins bins
    subsample: int, number of subsampled input point cloud
    """
    if subsample is not None:
        ids = np.random.choice(data.shape[0], subsample, replace=False)
        data = data[ids]
        color = color[ids]
    assert data.shape[0] == len(color)
    cmap = plt.cm.get_cmap('Spectral')
    c1, c2 = float(min(color)), float(max(color))
    color = (color-c1) / (c2-c1)
    EPS = 1e-4
    bins = np.linspace(-EPS, 1+EPS, num_bins+1)
    for i in xrange(num_bins):
        x = data[(color >= bins[i]) & (color < bins[i+1])]
        c = cmap(bins[i])[:3]
        mlab.points3d(x[:,0], x[:,1], x[:,2], color=c, scale_factor=0.01*size)
    if title:
        mlab.title(title)
    mlab.show()

def plot_pcd(pcd_filename, num_bins=50, subsample=None, size=1, title=''):
    from pclib import read_pcd
    pc, intensity = read_pcd(pcd_filename)
    plot_with_cmap(pc, intensity, num_bins=num_bins, subsample=subsample, size=size, title=title)

