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

def plot_pcd(pcd_filename, num_bins=10, subsample=20000, size=5, title=''):
    from pcplot import plot_with_cmap
    pc, intensity = read_pcd(pcd_filename)
    plot_with_cmap(pc, intensity, num_bins=num_bins, subsample=subsample, size=size, title=title)


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

def peak(vehicle, bag_name, ts_begin, camera=1, limit=1, tmp_dir='/home/xudong.sun/tmp', pc_viewer='mayavi', num_bins=10, subsample=20000, size=5, title=''):
    """
    peak dataset (camera and lidar) at a given timestamp
    vehicle: str, vehicle name, e.g. 'Octopus-B1'
    bag_name: str
    ts_begin: str or float, timestamp, e.g. 1552603966931801600, '30:00'
    camera: int, camera id
    limit: int, number of frames to show
    tmp_dir: save tmp files to this dir (will be cleaned)
    pc_viewer: 'mayavi' or 'pcl_viewer'
    """
    import os
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
    from pcplot import plot_with_cmap
    for data in ds.fetch_aligned(*topics, ts_begin=ts_begin, limit=limit):
        _check_fetched_ts(data)
        im = cv2.imdecode(np.fromstring(data[2][1].data, np.uint8), cv2.IMREAD_COLOR)
        out_path_im = os.path.join(tmp_dir, 'tmp.jpg')
        cv2.imwrite(out_path_im, im)
        p = subprocess.Popen(['eog', out_path_im])
        packet_left, packet_right = data[0][1], data[1][1]
        pc = pc_loader.grab([packet_left, packet_right])[0]
        pc, intensity = pc[:,:3], pc[:,3:]
        if pc_viewer == 'pcl_viewer':
            out_path_pc = os.path.join(tmp_dir, 'tmp.pcd')
            save_point_cloud_with_data(pc.astype(np.float64), intensity.astype(np.float64), out_path_pc, ASCIIFlag=True)
            subprocess.call(['pcl_viewer', out_path_pc])
            os.remove(out_path_pc)
        else:
            plot_with_cmap(pc, intensity, num_bins=num_bins, subsample=subsample, size=size, title=title)
        p.wait()
        os.remove(out_path_im)

