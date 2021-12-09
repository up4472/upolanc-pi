from library.methods_filter import color_balance_init
from library.methods_filter import color_balance_process_rgb565
from library.methods_filter import hue_saturation_init
from library.methods_filter import hue_saturation_process_rgb565
from library.methods_filter import lut_process_rgb565
from library.methods_filter import lut_init
from library.methods_filter import apply_rgb565_recoloring
from library.methods_color import transform_cv2_rgb565
from library.methods_color import transform_rgb565_cv2

import random
import numpy
import copy

class FilterManager :

	#
	# Creates a new filter manager object with the given configuration dictionary
	#

	def __init__ (self, config : dict) -> None :
		self.recolor_probability = config['recolor_probability']
		self.method = config['method']
		self.filter = 0
		self.filters = 34

		def private_method (index : int) -> float :
			return 1.785 * min(max((85 - index) / 64 + 0.5, 0), 1)

		self.shadows = [private_method(index = index) for index in range(256)]

	#
	# Select a filter based on the method type defined in the initialization
	#

	def select_filter (self) :
		if self.method == 'random' :
			self.filter = random.randrange(self.filters)

		if self.method == 'iterative' :
			self.filter = (self.filter + 1) % self.filters

	#
	# Applies the rgb565 filters to the image
	#

	def apply_rgb565_filters (self, image : numpy.ndarray, color : list = None) -> list :
		image = transform_cv2_rgb565(image = image)

		def private_method (data : numpy.ndarray) -> numpy.ndarray :
			self.select_filter()

			data = self.apply_rgb565_filter(image = data, color = color)

			return transform_rgb565_cv2(image = data)

		if random.random() < 0.75 :
			return [private_method(data = image)]

		return [private_method(data = copy.deepcopy(image)) for _ in range(4)]

	#
	# Applies the rgb565 filter to the image (same as efekti.c)
	#

	def apply_rgb565_filter (self, image : numpy.ndarray, color : list = None) -> numpy.ndarray :
		if self.filter == 0 :
			cblut = color_balance_init(red = 30, green = -32, blue = 16, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

		if self.filter == 1 :
			cblut = color_balance_init(red = -36, green = -37, blue = 39, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

		if self.filter == 2 :
			lvlut = lut_init(levels = 2)
			image = lut_process_rgb565(image = image, lut = lvlut)

		if self.filter == 3 :
			cblut = color_balance_init(red = 100, green = -100, blue = -100, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 3)
			image = lut_process_rgb565(image = image, lut = lvlut)

		if self.filter == 4 :
			cblut = color_balance_init(red = -100, green = -100, blue = 100, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 3)
			image = lut_process_rgb565(image = image, lut = lvlut)

		if self.filter == 5 :
			cblut = color_balance_init(red = -100, green = 100, blue = -100, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 3)
			image = lut_process_rgb565(image = image, lut = lvlut)

		if self.filter == 6 :
			lvlut = lut_init(levels = 5)
			image = lut_process_rgb565(image = image, lut = lvlut)

			hslut = hue_saturation_init(hue = -41, saturation = 6, value = -15)
			image = hue_saturation_process_rgb565(image = image, hue = hslut[0], saturation = hslut[1], value = hslut[2])

		if self.filter == 7 :
			lvlut = lut_init(levels = 6)
			image = lut_process_rgb565(image = image, lut = lvlut)

			cblut = color_balance_init(red = -29, green = 40, blue = 100, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

		if self.filter == 8 :
			hslut = hue_saturation_init(hue = -41, saturation = 25, value = -20)
			image = hue_saturation_process_rgb565(image = image, hue = hslut[0], saturation = hslut[1], value = hslut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

		if self.filter == 9 :
			cblut = color_balance_init(red = 100, green = -100, blue = -100, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 3)
			image = lut_process_rgb565(image = image, lut = lvlut)

			hslut = hue_saturation_init(hue = -41, saturation = 20, value = -10)
			image = hue_saturation_process_rgb565(image = image, hue = hslut[0], saturation = hslut[1], value = hslut[2])

		if self.filter == 10 :
			cblut = color_balance_init(red = 34, green = -38, blue = 24, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

			cblut = color_balance_init(red = -65, green = 0, blue = 0, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

		if self.filter == 11 :
			cblut = color_balance_init(red = 40, green = -40, blue = 28, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

			cblut = color_balance_init(red = -100, green = -42, blue = 35, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

		if self.filter == 12 :
			cblut = color_balance_init(red = 45, green = -45, blue = 35, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

		if self.filter == 13 :
			cblut = color_balance_init(red = 30, green = -35, blue = 20, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

		if self.filter == 14 :
			cblut = color_balance_init(red = 30, green = -32, blue = 16, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 15 :
			cblut = color_balance_init(red = -36, green = -37, blue = 39, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 16 :
			lvlut = lut_init(levels = 2)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = (2, 2))

		if self.filter == 17 :
			cblut = color_balance_init(red = 100, green = -100, blue = -100, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 3)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 18 :
			cblut = color_balance_init(red = -100, green = -100, blue = 100, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 3)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 19 :
			cblut = color_balance_init(red = -100, green = 100, blue = -100, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 3)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 20 :
			lvlut = lut_init(levels = 5)
			image = lut_process_rgb565(image = image, lut = lvlut)

			hslut = hue_saturation_init(hue = -41, saturation = 6, value = -15)
			image = hue_saturation_process_rgb565(image = image, hue = hslut[0], saturation = hslut[1], value = hslut[2])

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 21 :
			lvlut = lut_init(levels = 6)
			image = lut_process_rgb565(image = image, lut = lvlut)

			cblut = color_balance_init(red = -29, green = 40, blue = 100, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 22 :
			hslut = hue_saturation_init(hue = -41, saturation = 25, value = -20)
			image = hue_saturation_process_rgb565(image = image, hue = hslut[0], saturation = hslut[1], value = hslut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 23 :
			cblut = color_balance_init(red = 100, green = -100, blue = -100, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 3)
			image = lut_process_rgb565(image = image, lut = lvlut)

			hslut = hue_saturation_init(hue = -41, saturation = 20, value = -10)
			image = hue_saturation_process_rgb565(image = image, hue = hslut[0], saturation = hslut[1], value = hslut[2])

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 24 :
			cblut = color_balance_init(red = 34, green = -38, blue = 24, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

			hslut = hue_saturation_init(hue = -65, saturation = 0, value = 0)
			image = hue_saturation_process_rgb565(image = image, hue = hslut[0], saturation = hslut[1], value = hslut[2])

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 25 :
			cblut = color_balance_init(red = 40, green = -40, blue = 28, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

			cblut = color_balance_init(red = -100, green = -42, blue = 100, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 26 :
			cblut = color_balance_init(red = 45, green = -45, blue = 35, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 27 :
			cblut = color_balance_init(red = 30, green = -35, blue = 20, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		if self.filter == 28 :
			lvlut = lut_init(levels = 2)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = (3, 3))

		if self.filter == 29 :
			cblut = color_balance_init(red = 30, green = -35, blue = 20, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 4)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = (3, 3))

		if self.filter == 30 :
			lvlut = lut_init(levels = 3)
			image = lut_process_rgb565(image = image, lut = lvlut)

		if self.filter == 31 :
			cblut = color_balance_init(red = -100, green = -100, blue = 100, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 3)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = (4, 4))

		if self.filter == 32 :
			cblut = color_balance_init(red = 30, green = -40, blue = 16, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 3)
			image = lut_process_rgb565(image = image, lut = lvlut)

		if self.filter == 33 :
			cblut = color_balance_init(red = 30, green = -40, blue = 16, shadows = self.shadows)
			image = color_balance_process_rgb565(image = image, rlut = cblut[0], glut = cblut[1], blut = cblut[2])

			lvlut = lut_init(levels = 3)
			image = lut_process_rgb565(image = image, lut = lvlut)

			image = apply_rgb565_recoloring(image = image, color = color, location = None)

		return image
