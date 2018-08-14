import tensorflow as tf
import tensorlayer as tl
from tensorlayer.prepro import *
# from config import config, log_config
#
# img_path = config.TRAIN.img_path

import scipy
import numpy as np
import cv2
import numpy as np

def get_rand_offsets(img_h, img_w, wrg=384, hrg=384):
    h, w = img_h, img_w
    assert (h > hrg) and (w > wrg), "The size of cropping should smaller than the original image"
    h_offset = int(np.random.uniform(0, h - hrg) - 1)
    w_offset = int(np.random.uniform(0, w - wrg) - 1)
    return (h_offset, w_offset)

def get_imgs_fn(file_name, path):
    """ Input an image path and name, return an image array """
    # return scipy.misc.imread(path + file_name).astype(np.float)
    return scipy.misc.imread(path + file_name, mode='RGB')

def crop_sub_imgs_fn(x, is_random=True, h_offset=0, w_offset=0):
    if is_random is False:
        x = crop(x, wrg=384, hrg=384, is_random=is_random)
    else:
        wrg, hrg = 384, 384
        x = x[h_offset:hrg + h_offset, w_offset:wrg + w_offset]
    x = x / (255. / 2.)
    x = x - 1.
    return x

def downsample_fn(x):
    shapex,shapey,shapez = np.shape(x)
##    print("venkat",np.shape(x), type(x))

    if shapez is 3:
        # We obtained the LR images by downsampling the HR images using bicubic kernel with downsampling factor r = 4.
        x = imresize(x, size=[96, 96], interp='bicubic', mode=None)
        x = x / (255. / 2.)
        x = x - 1.
    elif shapez is 4:
        rgb = x[:,:,:-1]
        lir = x[:,:,3]
        sx,sy = np.shape(lir)
        lir=lir.reshape(sx,sy,1)
        
##        print("venkat2",np.shape(rgb))
##        print("venkat3",np.shape(lir))
        
        rgb = imresize(rgb, size=[96, 96], interp='bicubic', mode=None)
        rgb = rgb / (255. / 2.)
        rgb = rgb - 1.

        lir = imresize(lir, size=[96, 96], interp='bicubic', mode=None)
        lir = lir / (255. / 2.)
        lir = lir - 1.

        x = np.concatenate((rgb,lir),axis=2)
    else:
        print("invalid shape to downsample")
    return x

def downsample_by4_fn(x):
    shapex,shapey,shapez = np.shape(x)
##    print("venkat",np.shape(x), type(x))

    if shapez is 3:
        # We obtained the LR images by downsampling the HR images using bicubic kernel with downsampling factor r = 4.
        x = imresize(x, size=[shapex//4, shapey//4], interp='bicubic', mode=None)
        x = x / (255. / 2.)
        x = x - 1.
    elif shapez is 4:
        rgb = x[:,:,:-1]
        lir = x[:,:,3]
        sx,sy = np.shape(lir)
        lir=lir.reshape(sx,sy,1)
        
##        print("venkat2",np.shape(rgb))
##        print("venkat3",np.shape(lir))
        
        rgb = imresize(rgb, size=[shapex//4, shapey//4], interp='bicubic', mode=None)
        rgb = rgb / (255. / 2.)
        rgb = rgb - 1.

        lir = imresize(lir, size=[96, 96], interp='bicubic', mode=None)
        lir = lir / (255. / 2.)
        lir = lir - 1.

        x = np.concatenate((rgb,lir),axis=2)
    else:
        print("invalid shape to downsample")
    return x