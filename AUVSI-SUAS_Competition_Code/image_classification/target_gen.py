from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
import random
import webcolors

class target():
	def __init__(self, path, letter, letter_color, shape, shape_color, image, label):
		self.path = path
		self.letter = letter
		self.letter_color = letter_color
		self.shape = shape
		self.shape_color = shape_color
		self.label = label
		self.image = image

def replace_color(image_path, color):
	orig_color = "Black"
	img = Image.open(image_path).convert('RGB')
	pixdata = img.load()
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			if pixdata[x, y] == (0,0,0):
				pixdata[x, y] = webcolors.name_to_rgb(color)
	
	return img

def pair(k1, k2):
	return ((k1 + k2)*(k1 + k2 + 1))/2 + k2

def generate_image(requested_letter = None, requested_shape = None, requested_letter_color = None, requested_shape_color = None, requested_label = None, return_type = "target"):	
	letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	shape_list = ['Circle', 'Semicircle', 'Quartercircle', 'Triangle', 'Square', 'Rectangle', 'Trapezoid', 'Pentagon', 'Hexagon',
'Heptagon', 'Octagon', 'Star', 'Cross']
	color_list = ['White', 'Black', 'Gray', 'Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Brown', 'Orange']
	
	if (requested_letter == None):
		letter = letter_list[random.randrange(0,26)]
	else:
		letter = requested_letter

	if (requested_shape == None):
		shape_index = random.randrange(0,13)
		shape = shape_list[shape_index]
	else:
		shape = requested_shape
	
	if (requested_letter_color == None):
		letter_color_temp = random.randrange(0,10)
		letter_color = color_list[letter_color_temp]
	else:
		letter_color = requested_letter_color
		letter_color_temp = color_list.index(letter_color)
	
	if (requested_shape_color == None):
		shape_color_temp = random.randrange(0,10)
		while (shape_color_temp == letter_color_temp):
			shape_color_temp = random.randrange(0,10)
		shape_color = color_list[shape_color_temp]
	else:
		shape_color = requested_shape_color

	background_path = 'Grass.png'
	letter_path = letter + '.png'
	shape_path = 'shapes/' + shape + '.png'
	composite_path = letter_color + "_" + letter + "_" + shape_color + "_" + shape + ".png"

	composite = Image.open(background_path)
	shape_temp = Image.open(shape_path)
	composite.paste(replace_color(shape_path, shape_color), (64,64), shape_temp)
	temp = ImageDraw.Draw(composite)
	font = ImageFont.truetype("LiberationMono-Bold.ttf", 64)
	W, H = 256, 256
	w, h = temp.textsize(letter)
	temp.text((108, 99),letter,letter_color,font=font)
	composite = composite.filter(ImageFilter.EDGE_ENHANCE)
	composite = composite.resize((64,64), Image.ANTIALIAS)
	composite.save('composites/'+composite_path)
	image = composite.convert("RGBA")
	
	#if (requested_label == 'shape'):
	#	label = shape_list.index(shape)
	#elif (requested_label == 'letter'):
	#	label = letter_list.index(letter)+14
	label = [0] * 729
	label[pair(shape_list.index(shape),letter_list.index(letter))] = 1
	#print(label.index(1))
	
	if (return_type == "target"):
		return target(composite_path, letter, letter_color, shape, shape_color, image, label)
	elif (return_type == "set"):
		return image, label



