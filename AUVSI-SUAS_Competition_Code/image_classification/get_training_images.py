import tflearn
import numpy as np
from tflearn.data_utils import shuffle
from tflearn.data_utils import *
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import pickle
import target_gen
from PIL import Image
from PIL import ImageFilter
import sys
np.set_printoptions(threshold=np.inf)
# load dataset of auvsi targets
# or generate them on demand here??
num_testing_images = 100
if sys.argv[1]:
	num_testing_images = int(sys.argv[1])

print("generating " + str(num_testing_images) + " testing images")
for i in range(0, num_testing_images):
	tmp_img, tmp_label = target_gen.generate_image(return_type = "shape")
