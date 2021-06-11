import sys
import os
import numpy as np
from PIL import Image, ImageOps

ARDUINO_PATH = 'oscil_img/oscil_img.ino'

def main(image_name):
	# Search for the image file
	files = os.listdir('images')
	for file in files:
		if image_name in file:
			image_name = file
			break

	# First import image
	orig_image = Image.open('images/' + image_name)

	# Convert to grayscale
	gray_image = ImageOps.grayscale(orig_image)

	# Figure out what dimensions we need via the arduino file
	rows = -1
	cols = -1
	list_of_lines = []
	with open(ARDUINO_PATH) as file:
		list_of_lines = file.readlines()
		for line in list_of_lines:
			if line[:13] == '#define X_RES':
				cols = int(line[13:])
			elif line[:13] == '#define Y_RES':
				rows = int(line[13:])
			if rows > -1 and cols > -1:
				break
	# Make sure the dimensions were defined
	if rows < 0 or cols < 0:
		print('Make sure to define dimensions in the Arduino file')
	
	# Resize image to the desired size
	gray_image = gray_image.resize((cols, rows))

	# Convert to numpy array
	np_img = np.array(gray_image)

	# Construct the array as a C 2d array
	c_img_arr = 'const uint8_t pixel_map[Y_RES][X_RES] =\n{\n'
	for r in range(rows):
		c_img_arr += '\t{'
		for c in range(cols - 1):
			c_img_arr += str(np_img[r, c]) + ', '
		if r < rows - 1:
			c_img_arr += str(np_img[r, c]) + '},\n'
		else:
			c_img_arr += str(np_img[r, c]) + '}\n};\n'
	
	# Replace the old image 2d array with the new one
	new_lines = []
	keep = True
	for line in list_of_lines:
		if 'const uint8_t pixel_map' in line:
			keep = False
		elif len(line) > 2 and line[-2] == ';' and keep == False:
			keep = True
			new_lines += c_img_arr.splitlines(keepends=True)
		elif keep:
			new_lines.append(line)

	# Update the file
	with open(ARDUINO_PATH, 'w') as file:
		file.writelines(new_lines)

if __name__ == '__main__':
	assert len(sys.argv) == 2
	main(sys.argv[1])