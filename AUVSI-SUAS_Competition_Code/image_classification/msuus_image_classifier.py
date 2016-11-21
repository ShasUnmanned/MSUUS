import tflearn
import numpy as np
from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import pickle
import target_gen

# load dataset of auvsi targets
# or generate them on demand here??
num_training_images = 1000
num_testing_images = 100
images = [None] * num_training_images
labels = [None] * num_training_images
images_test = [None] * num_testing_images
labels_test = [None] * num_testing_images

for i in range(0, num_training_images):
	tmp_img, tmp_label = target_gen.generate_image(return_type = "set")
	images[i] = np.reshape(tmp_img.getdata(), (64, 64, -1))
	labels[i] = np.reshape(tmp_label, (-1))

for i in range(0, num_testing_images):
	tmp_img, tmp_label = target_gen.generate_image(return_type = "set")
	images_test[i] = np.reshape(tmp_img.getdata(), (64, 64, -1))
	labels_test[i] = np.reshape(tmp_label, (-1))

# shuffle images
images, labels = shuffle(images, labels)

# create preprocessor to normalize images
img_preprocessor = ImagePreprocessing()
img_preprocessor.add_featurewise_zero_center()
img_preprocessor.add_featurewise_stdnorm()

# distort images
img_distortion = ImageAugmentation()

# only flip left/right for shape training
#img_distortion.add_random_flip_leftright()

img_distortion.add_random_rotation(max_angle=360.)
img_distortion.add_random_blur(sigma_max=3.)



###
### network architecture
###

network = input_data(shape=[None, 64, 64, 4], 
	data_preprocessing=img_preprocessor,
	data_augmentation=img_distortion)

# convolution 
network = conv_2d(network, 128, 3, activation='relu')

# max pooling
network = max_pool_2d(network, 2)

# convolution 2
network = conv_2d(network, 256, 3, activation='relu')

# convolution 3
network = conv_2d(network, 256, 3, activation='relu')

# max pooling 2
network = max_pool_2d(network, 2)

# fully-connected
network = fully_connected(network, 1024, activation='relu')

# dropout
network = dropout(network, 0.5)

# fully-connected final
network = fully_connected(network, 2, activation='softmax')


network = regression(network, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.001)


model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='/media/salvi/E4D81381D81350E2/checkpoints/msuus-target-classifier.tfl.ckpt')

model.fit(images, labels, n_epoch=50, shuffle=True, validation_set=(images_test, labels_test), show_metric=True, batch_size=64, snapshot_epoch=True, run_id='msuus-target-classifier')

model.save("msuus-target-classifier.tfl")
print("Network trained and saved as msuus-target-classifier.tfl")

