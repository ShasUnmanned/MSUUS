import target_gen
import sys
num_testing_images = 100
if sys.argv[1]:
	num_testing_images = int(sys.argv[1])

for i in range(0, num_testing_images):
	tmp_img, tmp_label = target_gen.generate_image(return_type = "shape")
	sys.stdout.write("Generating image %d/%d	 \r" % (i, num_testing_images) )
	sys.stdout.flush()
sys.stdout.write("Generating image %d/%d \n" % (i+1, num_testing_images) )
sys.stdout.write("Finished generating images\n")
