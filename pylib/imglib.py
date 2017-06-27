'''
image processing utilities
'''

import cv2

def gaussian_blur(img, kernel_size):
    '''apply Gaussian blur on img
    kernal_size: Gaussian kernel size, must be an odd number. e.g. 21
    '''
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0, 0)

def pepper_and_salt(img, noise_level):
    '''apply pepper and salt noise on img
    noise_level: a floating-point number [0, 1], e.g. 0.05
    '''
    import random
    new_img = img.copy()
    height, width = img.shape[:2]
    for i in xrange(int(round(noise_level * img.size))):
        new_img[random.randint(0, height - 1), random.randint(0, width - 1), random.randint(0, 2)] = 255 * (i % 2)
    return new_img


