import tflearn

from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import pickle

# load dataset of auvsi targets
# or generate them on demand here??
image, label, image_test, label_test = pickle.load(open("auvsi_target_dataset.pkl", "rb"))

# shuffle images
image, label = shuffle(image, label)

# create preprocessor to normalize images
img_preprocessor = ImagePreprocessing()
img_preprocessor.add_featurewise_zero_center()
img_preprocessor.add_featurewise_stdnorm()

# distort images
img_distortion = ImageAugmentation()

# only flip left/right for shape training
img_distortion.add_random_flip_leftright()

img_distortion.add_random_rotation(max_angle=360.)
img_distortion.add_random_blur(sigma_max=3.)



###
### network architecture
###

network = input_data(shape=[None, 
