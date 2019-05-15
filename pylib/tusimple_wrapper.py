import os
import numpy as np

######################################
# pcd utilities
######################################

def read_pcd(pcd_filename):
    from py_lidar_bind import get_single_point_cloud
    pcd = get_single_point_cloud(pcd_filename)
    pc = pcd[0]
    intensity = pcd[1][:,0]
    return pc, intensity

def save_pcd(filename, pc, intensity=None, label=None, ASCIIFlag=True):
    """
    pc: ndarray, (N, 3)
    intensity: ndarray, (N,)
    """
    if intensity is None and label is None:
        from py_lidar_bind import save_point_cloud
        save_point_cloud(pc.astype(np.float64), filename, ASCIIFlag=ASCIIFlag)
    else:
        data = np.zeros((pc.shape[0], 3))
        if intensity is not None:
            data[:,0] = intensity
        if label is not None:
            data[:,2] = label
        else:
            data[:,2] = np.ones(pc.shape[0])
        from py_lidar_bind import save_point_cloud_with_data
        save_point_cloud_with_data(pc.astype(np.float64), data.astype(np.float64), filename, ASCIIFlag=ASCIIFlag)

def plot_pcd(pcd_filename, bg=False):
    import subprocess
    cmd_args = ['pcl_viewer', pcd_filename]
    if bg:
        p = subprocess.Popen(cmd_args)
        return p
    else:
        subprocess.call(cmd_args)

def plot_pc(pc, intensity=None, label=None, bg=False):
    """
    bg: if True, plot pc in a separate process and return the process
    """
    tmp_pcd_filename = os.path.join(os.environ['HOME'], 'tmp', 'tmp.pcd')
    save_pcd(tmp_pcd_filename, pc, intensity, label)
    p = plot_pcd(tmp_pcd_filename, bg)
    return p

def plot_img(img, bg=False):
    import subprocess
    import cv2 as cv
    tmp_img_filename = os.path.join(os.environ['HOME'], 'tmp', 'tmp.jpg')
    cv.imwrite(tmp_img_filename, img)
    cmd_args = ['eog', tmp_img_filename]
    if bg:
        p = subprocess.Popen(cmd_args)
        return p
    else:
        subprocess.call(cmd_args)

def plot_pc_with_image(pc, intensity=None, label=None, img=None):
    p = plot_pc(pc, intensity, label, bg=True)
    if img is not None:
        plot_img(img)
    p.wait()


#######################################
# Dataset utilities
#######################################

def _check_fetched_ts(data, threshold=0.05):
    """
    check ts from fetched data, make sure the data is correctly aligned
    data: return value from Dataset.fetch_aligned
    threshold: maximum ts misalignment (seconds)
    return: boolean
    """
    ts = data[0][0] / 1e9
    flag = True
    for t, _ in data:
        if abs(t/1e9 - ts) > threshold:
            print "dataset is not correctly aligned at ts = {}".format(ts)
            flag = False
    return flag

def peak(vehicle, bag_name, ts_begin, camera=1, limit=1,
         x=None, y=None, z=None, intensity=None):
    """
    peak dataset (camera and lidar) at a given timestamp
    vehicle: str, vehicle name, e.g. 'Octopus-B1'
    bag_name: str
    ts_begin: str or float, timestamp, e.g. 1552603966931801600, '30:00'
    camera: int, camera id
    limit: int, number of frames to show
    x, y, z, intensity: list of length 2, [min, max] range
    pc_viewer: 'mayavi' or 'pcl_viewer'
    """
    import cv2
    import subprocess
    topics = ['/pandar_left/pandar_packets', '/pandar_right/pandar_packets', '/camera{}/image_color/compressed'.format(camera)]
    # get correction and calibration info
    from calibration_manager import CalibrationManager
    calib_manager = CalibrationManager({'vehicle': vehicle, 'bag_name': bag_name})
    lidar_calibs = calib_manager.get_lidars()
    intrinsic_file_paths = [lidar_calibs[i]['intrinsic_file_path'] for i in (1,2)]
    extrinsic_matrices = [lidar_calibs[i]['extrinsic']['imu-0'] for i in (1,2)]
    # Loader for lidar packets to point cloud
    from py_lidar.loader import CLoader
    from py_lidar_bind import save_point_cloud_with_data
    pc_loader = CLoader(intrinsic_file_paths, extrinsic_matrices, lidar_type='Pandar40')
    # fetch dataset
    from dataset_store import Dataset
    ds = Dataset.open(bag_name)
    for data in ds.fetch_aligned(*topics, ts_begin=ts_begin, limit=limit):
        _check_fetched_ts(data)
        im = cv2.imdecode(np.fromstring(data[2][1].data, np.uint8), cv2.IMREAD_COLOR)
        packet_left, packet_right = data[0][1], data[1][1]
        pc = pc_loader.grab([packet_left, packet_right])[0]
        pc, intensity = pc[:,:3], pc[:,3]
        # mask
        mask = np.ones(pc.shape[0], dtype=np.bool)
        if x is not None:
            mask &= (pc[:,0] >= x[0]) & (pc[:,0] <= x[1])
        if y is not None:
            mask &= (pc[:,1] >= y[0]) & (pc[:,1] <= y[1])
        if z is not None:
            mask &= (pc[:,2] >= z[0]) & (pc[:,2] <= z[1])
        if intensity is not None:
            mask &= (data_[:,0] >= intensity[0]) & (data_[:,0] <= intensity[1])
        pc, intensity = pc[mask], intensity[mask]
        plot_pc_with_image(pc, intensity, None, im)

