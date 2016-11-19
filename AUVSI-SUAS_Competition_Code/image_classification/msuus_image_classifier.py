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
images, labels, images_test, labels_test = pickle.load(open("auvsi_target_dataset.pkl", "rb"))

# shuffle images
images, labels = shuffle(images, labels)

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

network = input_data(shape=[None, 64, 64, 3], 
	data_preprocessing=img_preprocessor,
	data_augmentation=img_distortion)

# convolution 
network = conv_2d(network, 64, 3, activation='relu')

# max pooling
network = max_pool_2d(network, 2)

# convolution 2
network = conv_2d(network, 128, 3, activation='relu')

# convolution 3
network = conv_2d(network, 128, 3, activation='relu')

# max pooling 2
network = max_pool_2d(network, 2)

# fully-connected
network = fully_connected(network, 1024, activation='relu')

# dropout
network = regression(network, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.001)


model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='msuus-target-classifier.tfl.ckpt')

model.fit(images, labels, n_epoch=100, shuffle=True, validation_set=(images_test, labels_test), show_metric=True, batch_size=64, snapshot_epoch=True, run_id='msuus-target-classifier')

model.save("msuus-target-classifier.tfl")
print("Network trained and saved as msuus-target-classifier.tfl")







