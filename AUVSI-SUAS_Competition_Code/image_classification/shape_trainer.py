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
from PIL import ImageEnhance
from PIL import ImageFilter
np.set_printoptions(threshold=np.inf)
# load dataset of auvsi targets
# or generate them on demand here??
num_variations = 2
num_training_images = int(26*13)*num_variations
num_testing_images = 640
#images = [None] * num_training_images
#labels = [None] * num_training_images
images_test = [None] * num_testing_images
labels_test = [None] * num_testing_images


letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

shape_list = ['Circle', 'Semicircle', 'Quartercircle', 'Triangle', 'Square', 'Rectangle', 'Trapezoid', 'Pentagon', 'Hexagon', 'Heptagon', 'Octagon', 'Star', 'Cross']


counter = 0
'''
for q in range(0, num_variations):
	for i in range(0, 26):
		for a in range(0, 13):
			tmp_img, tmp_label = target_gen.generate_image(requested_letter=letter_list[i], 
				requested_shape=shape_list[a], 
				#requested_letter_color="White", 
				#requested_shape_color="Black", 
				return_type = "shape")
		
			#for q in range(0, num_variations):
			tmp_img_2 = tmp_img
			tmp_img_2 = tmp_img_2.filter(ImageFilter.SMOOTH_MORE)
			tmp_img_2 = tmp_img_2.convert('L')
			tmp_img_2 = tmp_img_2.filter(ImageFilter.EDGE_ENHANCE_MORE)
			images[counter] = np.reshape(tmp_img_2.getdata(), (64, 64, -1))
			labels[counter] = np.zeros(13)
			labels[counter][tmp_label] = 1
			#print(str(labels[counter]))
			ls_str = 'letter ' + letter_list[i]
			print(ls_str + ", shape " + shape_list[a] + ' variation ' + str(q))

			counter += 1
			#if (q == 0 and i == 0):
			#	tmp_img_2.show()
'''

# load images
dataset_file = 'composites/'

print("loading image dataset")
x, labels = image_preloader(dataset_file, image_shape=(64, 64), mode='folder', categorical_labels=True, normalize=False)

images = [None] * len(x)

for i in range(0, len(x)):
	temp = x[i]
	images[i] = np.uint8(temp) 
	images[i] = Image.fromarray(images[i])
	images[i] = images[i].convert('L')
	enh_c = ImageEnhance.Contrast(images[i])
	images[i] = enh_c.enhance(12.0)
	images[i] = images[i].filter(ImageFilter.SMOOTH_MORE)
	images[i] = images[i].filter(ImageFilter.SMOOTH_MORE)
	images[i] = images[i].filter(ImageFilter.EDGE_ENHANCE_MORE)
	images[i] = images[i].filter(ImageFilter.SMOOTH_MORE)
	images[i] = images[i].filter(ImageFilter.EDGE_ENHANCE_MORE)
	#if i % 1000 == 0:
		#images[i].show()
	tmp_arr = np.fromstring(images[i].tobytes(), np.uint8)
	images[i] = tmp_arr.reshape(64,64,1)	
	#images[i] = np.reshape(tmp_arr, (64, 64, -1))


print("generating " + str(num_testing_images) + " testing images")
for i in range(0, num_testing_images):
	tmp_img, tmp_label = target_gen.generate_image(return_type = "shape")
	tmp_img = tmp_img.convert('L')
	enh_c = ImageEnhance.Contrast(tmp_img)
	tmp_img = enh_c.enhance(12.0)
	tmp_img = tmp_img.filter(ImageFilter.SMOOTH_MORE)
	tmp_img = tmp_img.filter(ImageFilter.SMOOTH_MORE)
	tmp_img = tmp_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
	tmp_img = tmp_img.filter(ImageFilter.SMOOTH_MORE)
	tmp_img = tmp_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
	#if i == 1:
		#tmp_img.show()
	tmp_arr = np.fromstring(tmp_img.tobytes(), np.uint8)
	images_test[i] = tmp_arr.reshape(64,64,1)
	labels_test[i] = np.zeros(13)
	labels_test[i][tmp_label] = 1.

# shuffle images
print("shuffling images")
images, labels = shuffle(images, labels)
images_test, labels_test = shuffle(images_test, labels_test)

# create preprocessor to normalize images
print("creating preprocessor")
img_preprocessor = ImagePreprocessing()
img_preprocessor.add_featurewise_zero_center()
img_preprocessor.add_featurewise_stdnorm()

# distort images
print("adding distortion")
img_distortion = ImageAugmentation()

# only flip left/right for shape training
#img_distortion.add_random_flip_leftright()
#img_distortion.add_random_blur(sigma_max=1.)



###
### network architecture
###
print("setting up network")
network = input_data(shape=[None, 64, 64, 1], 
	data_preprocessing=img_preprocessor,
	data_augmentation=img_distortion)


# convolution 2
network = conv_2d(network, 16, 5, activation='relu')
# max pooling 2
network = max_pool_2d(network, 2)
# convolution 2
network = conv_2d(network, 16, 5, activation='relu')
# max pooling 2
network = max_pool_2d(network, 2)
# convolution 2
network = conv_2d(network, 16, 5, activation='relu')
# max pooling 2
network = max_pool_2d(network, 2)
# fully-connected
network = fully_connected(network,128, activation='relu')
# fully-connected
network = fully_connected(network,128, activation='relu')

# dropout
network = dropout(network, 0.5)

# fully-connected final
network = fully_connected(network, 13, activation='softmax')


network = regression(network, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.0001)


model = tflearn.DNN(network, tensorboard_verbose=2, checkpoint_path='/media/salvi/E4D81381D81350E2/checkpoints/shape_classifier.tfl.ckpt')

# if previously trained model is available use that
model.load('shape_classifier.tfl')

model.fit(images, labels, n_epoch=50, shuffle=True, validation_set=(images_test, labels_test), show_metric=True, batch_size=128, snapshot_epoch=True, run_id='shape_classifier')

model.save("shape_classifier.tfl")
print("Network trained and saved as shape_classifier.tfl")

