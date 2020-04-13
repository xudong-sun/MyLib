#########################################
# plot point cloud with mayavi.mlab
#########################################

import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab

def _plot_color(data, label, scale_factor, color={}):
    if color == {}:
        color = {0: (0,1,1), 1: (1,0,0), 2: (1,1,0), 3: (0,1,0),
                 4: (0,0,1), 5: (1,0,1), 6: (0.4, 0.7, 0.6), 7: (0.5, 0, 0.6),
                 8: (0.99, 0.88, 0.55), 9: (0.96, 0.4, 0.3), 10: (0.6, 0, 0.2),
                 11: (0,1,0.8)}
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
    if subsample is not None and subsample < data.shape[0]:
        ids = np.random.choice(data.shape[0], subsample, replace=False)
        data = data[ids]
    mlab.points3d(data[:,0], data[:,1], data[:,2], scale_factor=0.01*size)
    if title:
        mlab.title(title)
    mlab.show()

def plot_with_labels(data, label, subsample=None, size=1, color={}, title='', img=None, img_path=None):
    """
    data: Nx3 numpy array
    label: N, numpy array
    subsample: number of subsampled input point cloud
    size: size of points
    color: dict int->tuple(3)
    """
    if img is not None:
        img_path = os.path.join(os.environ['HOME'], 'tmp', 'tmp.jpg')
        cv.imwrite(img_path, img)
    if img_path is not None:
        p = subprocess.Popen(['eog', img_path])
    if subsample is not None and subsample < data.shape[0]:
        ids = np.random.choice(data.shape[0], subsample, replace=False)
        data = data[ids]
        label = label[ids]
    _plot_color(data, label, 0.01*size, color=color)
    if title:
        mlab.title(title)
    mlab.show()
    if img_path is not None:
        p.wait()

def plot_with_cmap(data, color, num_bins=10, subsample=None, size=1, title=''):
    """
    data: Nx3 numpy array
    color: N, numpy array
    num_bins: int, discretize color into num_bins bins
    subsample: int, number of subsampled input point cloud
    """
    if subsample is not None and subsample < data.shape[0]:
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
        c = cmap(1-bins[i])[:3]
        mlab.points3d(x[:,0], x[:,1], x[:,2], color=c, scale_factor=0.01*size)
    if title:
        mlab.title(title)
    mlab.show()

