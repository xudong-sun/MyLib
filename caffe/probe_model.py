import _init_paths
import caffe
from commons import check_file_exists

MODEL = 'pvanet_frcnn_iter_1.caffemodel'
prototxt = '/home/deepir/dev/DeepirFace/FaceDetection/pva-faster-rcnn-alignment/models/pvanet/example_train/train.prototxt'

if __name__ == '__main__':
    for file_ in (MODEL, prototxt): check_file_exists(file_)
    net = caffe.Net(prototxt, MODEL, caffe.TEST)
    
    # blob shapes
    print '***** blobs *****'
    for blob_name in net.blobs:
        print blob_name, [val for val in net.blobs[blob_name].shape]

    # params
    print '***** params *****'
    for layer_name in net.params:
        print layer_name
        print 'weights', [val for val in net.params[layer_name][0].shape]
        if len(net.params[layer_name]) > 1: print 'bias', [val for val in net.params[layer_name][1].shape]

