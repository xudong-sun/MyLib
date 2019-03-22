import numpy as np


#################################
# point cloud transformation
#################################

def normalize_point_cloud(pc):
    """
    Normalize a point cloud: mean-shift + variance
    Input: Nx3 point cloud
    Return: Nx3 normalized
    """
    l = pc.shape[0]
    centroid = np.mean(pc, axis=0)
    pc = pc - centroid
    m = np.max(np.sqrt(np.sum(pc**2, axis=1)))
    pc = pc / m
    return pc

def rotate_point_cloud_y(batch_data):
    """
    Randomly rotate the point clouds around y axis to augument the dataset
    rotation is per shape based along up direction
    Input:
      BxNx3 array, original batch of point clouds
    Return:
      BxNx3 array, rotated batch of point clouds
    """
    rotated_data = np.zeros(batch_data.shape, dtype=np.float32)
    for k in xrange(batch_data.shape[0]):
        rotation_angle = np.random.uniform() * 2 * np.pi
        cosval = np.cos(rotation_angle)
        sinval = np.sin(rotation_angle)
        rotation_matrix = np.array([[cosval, 0, sinval],
                                    [0, 1, 0],
                                    [-sinval, 0, cosval]])
        shape_pc = batch_data[k, ...]
        rotated_data[k, ...] = np.dot(shape_pc.reshape((-1, 3)), rotation_matrix)
    return rotated_data

def rotate_point_cloud_z(batch_data):
    """
    Randomly rotate the point clouds around z axis to augument the dataset
    rotation is per shape based along up direction
    Input:
      BxNx3 array, original batch of point clouds
    Return:
      BxNx3 array, rotated batch of point clouds
    """
    rotated_data = np.zeros(batch_data.shape, dtype=np.float32)
    for k in xrange(batch_data.shape[0]):
        rotation_angle = np.random.uniform() * 2 * np.pi
        cosval = np.cos(rotation_angle)
        sinval = np.sin(rotation_angle)
        rotation_matrix = np.array([[cosval, -sinval, 0],
                                    [sinval, cosval, 0],
                                    [0, 0, 1]])
        shape_pc = batch_data[k, ...]
        rotated_data[k, ...] = np.dot(shape_pc.reshape((-1, 3)), rotation_matrix)
    return rotated_data

def rotate_point_cloud_by_angle(batch_data, rotation_angle):
    """
    Rotate the point cloud along up direction with certain angle.
    Input:
      BxNx3 array, original batch of point clouds
    Return:
      BxNx3 array, rotated batch of point clouds
    """
    rotated_data = np.zeros(batch_data.shape, dtype=np.float32)
    for k in xrange(batch_data.shape[0]):
        #rotation_angle = np.random.uniform() * 2 * np.pi
        cosval = np.cos(rotation_angle)
        sinval = np.sin(rotation_angle)
        rotation_matrix = np.array([[cosval, 0, sinval],
                                    [0, 1, 0],
                                    [-sinval, 0, cosval]])
        shape_pc = batch_data[k,:,0:3]
        rotated_data[k,:,0:3] = np.dot(shape_pc.reshape((-1, 3)), rotation_matrix)
    return rotated_data

def rotate_perturbation_point_cloud(batch_data, angle_sigma=0.06, angle_clip=0.18):
    """
    Randomly perturb the point clouds by small rotations
    Input:
      BxNx3 array, original batch of point clouds
    Return:
      BxNx3 array, rotated batch of point clouds
    """
    rotated_data = np.zeros(batch_data.shape, dtype=np.float32)
    for k in xrange(batch_data.shape[0]):
        angles = np.clip(angle_sigma*np.random.randn(3), -angle_clip, angle_clip)
        Rx = np.array([[1,0,0],
                       [0,np.cos(angles[0]),-np.sin(angles[0])],
                       [0,np.sin(angles[0]),np.cos(angles[0])]])
        Ry = np.array([[np.cos(angles[1]),0,np.sin(angles[1])],
                       [0,1,0],
                       [-np.sin(angles[1]),0,np.cos(angles[1])]])
        Rz = np.array([[np.cos(angles[2]),-np.sin(angles[2]),0],
                       [np.sin(angles[2]),np.cos(angles[2]),0],
                       [0,0,1]])
        R = np.dot(Rz, np.dot(Ry,Rx))
        shape_pc = batch_data[k, ...]
        rotated_data[k, ...] = np.dot(shape_pc.reshape((-1, 3)), R)
    return rotated_data

def jitter_point_cloud(batch_data, sigma=0.01, clip=0.05):
    """
    Randomly jitter points. jittering is per point.
    Input:
      BxNx3 array, original batch of point clouds
    Return:
      BxNx3 array, jittered batch of point clouds
    """
    B, N, C = batch_data.shape
    assert(clip > 0)
    jittered_data = np.clip(sigma * np.random.randn(B, N, C), -1*clip, clip)
    jittered_data += batch_data
    return jittered_data

def shift_point_cloud(batch_data, shift_range=0.1):
    """
    Randomly shift point cloud. Shift is per point cloud.
    Input:
      BxNx3 array, original batch of point clouds
    Return:
      BxNx3 array, shifted batch of point clouds
    """
    B, N, C = batch_data.shape
    shifts = np.random.uniform(-shift_range, shift_range, (B,3))
    for batch_index in range(B):
        batch_data[batch_index,:,:] += shifts[batch_index,:]
    return batch_data

def random_scale_point_cloud(batch_data, scale_low=0.8, scale_high=1.25):
    """
    Randomly scale the point cloud. Scale is per point cloud.
    Input:
      BxNx3 array, original batch of point clouds
    Return:
      BxNx3 array, scaled batch of point clouds
    """
    B, N, C = batch_data.shape
    scales = np.random.uniform(scale_low, scale_high, B)
    for batch_index in range(B):
        batch_data[batch_index,:,:] *= scales[batch_index]
    return batch_data

def shuffle_points(batch_data, batch_label=None):
    """
    Shuffle orders of points in each point cloud -- changes FPS behavior.
    Use the same shuffling idx for the entire batch.
    May optionally pass in the per-point label
    Input:
      BxNxC array, batch_data
      BxN array, batch_label, optional
    Output:
      BxNxC array, shuffled batch_data
      BxN, shuffled batch_label, if it is present
    """
    idx = np.arange(batch_data.shape[1])
    np.random.shuffle(idx)
    if batch_label is None:
        return batch_data[:,idx,:]
    else:
        return batch_data[:,idx,:], batch_label[:,idx]

def random_point_dropout(batch_pc, labels=None, max_dropout_ratio=0.875):
    """
    batch_pc: BxNx3
    labels: [optional] BxN, per point label
    """
    for b in range(batch_pc.shape[0]):
        dropout_ratio =  np.random.random()*max_dropout_ratio
        drop_idx = np.where(np.random.random((batch_pc.shape[1]))<=dropout_ratio)[0]
        if len(drop_idx)>0:
            batch_pc[b,drop_idx,:] = batch_pc[b,0,:] # set to the first point
            if labels is not None:
                labels[b,drop_idx] = labels[b,0]
    if labels is not None:
        return batch_pc, labels
    else:
        return batch_pc


#######################################
# point cloud -> voxel
#######################################

def point_cloud_label_to_surface_voxel_label(point_cloud, label, res=0.02):
    """
    point cloud to voxel
    Input:
        point_cloud: Nx3
        label: N, or Nx2
    Output:
        uvidx: keep ids when converting to voxel, (M,)
        uvlabel: labels of the kept indices, (M,) or (M,2)
    """
    coordmax = np.max(point_cloud, axis=0)
    coordmin = np.min(point_cloud, axis=0)
    nvox = np.ceil((coordmax - coordmin) / res)
    vidx = np.ceil((point_cloud - coordmin) / res)
    vidx = vidx[:,0] + vidx[:,1]*nvox[0] + vidx[:,2]*nvox[0]*nvox[1]
    uvidx, vpidx = np.unique(vidx, return_index=True)
    uvlabel = label[vpidx]
    return uvidx, uvlabel


