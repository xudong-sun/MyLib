import os.path as osp
import sys

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)

# Add caffe to PYTHONPATH
#caffe_path = '/home/deepir/software/caffe/python'
caffe_path = '/home/deepir/dev/DeepirFace/FaceDetection/pva-faster-rcnn/caffe-fast-rcnn/python'
add_path(caffe_path)

lib_path = '/home/deepir/dev/DeepirFace/FaceDetection/pva-faster-rcnn/lib'
add_path(lib_path)
