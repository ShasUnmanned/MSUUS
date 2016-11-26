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
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance

tmp_img = Image.open("test_image.png")
tmp_img = tmp_img.resize((64,64), Image.ANTIALIAS)

enh_c = ImageEnhance.Contrast(tmp_img)
tmp_img = enh_c.enhance(5.0)

tmp_img = tmp_img.convert('L')
tmp_img = tmp_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
tmp_img = tmp_img.point(lambda x: 0 if x<128 else 255, '1')
tmp_img.show()
image = np.reshape(tmp_img.getdata(), (64, 64, -1))

###
### network architecture
###

img_preprocessor = ImagePreprocessing()

img_distortion = ImageAugmentation()

network = input_data(shape=[None, 64, 64, 1], 
	data_preprocessing=img_preprocessor,
	data_augmentation=img_distortion)
network = conv_2d(network, 64, 4, activation='relu')
network = max_pool_2d(network, 2)
network = conv_2d(network, 96, 4, activation='relu')
network = conv_2d(network, 128, 4, activation='relu')
network = max_pool_2d(network, 2)
network = fully_connected(network, 512, activation='relu')
network = dropout(network, 0.5)
network = fully_connected(network, 2, activation='softmax')
network = regression(network, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.001)


model = tflearn.DNN(network, tensorboard_verbose=2, checkpoint_path='/media/salvi/E4D81381D81350E2/checkpoints/msuus-target-classifier.tfl.ckpt')
model.load('msuus-target-classifier.tfl.ckpt-2286')

predicted_target_label = model.predict([image])

print(predicted_target_label)

