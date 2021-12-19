from library.methods_filter import color_balance
from library.methods_filter import hue_saturation
from library.methods_filter import posterize
from library.methods_filter import recoloring

from typing import List
from typing import Dict
from typing import Any

import random
import numpy
import copy

class FilterManager :

	#
	# Creates a new filter manager object with the given configuration dictionary
	#

	def __init__ (self, config : Dict[str, Any]) -> None :
		self.method = config['method']
		self.filter = -1
		self.filters = 34

	#
	# Select and apply filter to the image
	#

	def apply_filters (self, image : numpy.ndarray, color : List[int] = None) -> List[numpy.ndarray] :
		def process_image (image : numpy.ndarray) -> numpy.ndarray :
			self.select_filter()

			return self.apply_filter(image = image, color = color)

		if random.random() < 0.75 :
			return [process_image(image = image)]

		return [process_image(image = copy.deepcopy(image)) for _ in range(4)]

	#
	# Select a filter based on the method type defined in the initialization
	#

	def select_filter (self) -> None :
		if self.method == 'random' :
			self.filter = random.randrange(self.filters)

		if self.method == 'iterative' :
			self.filter = (self.filter + 1) % self.filters

		print(f'Selected filter : {self.filter}')

	#
	# Apply filter to the image
	#

	def apply_filter (self, image : numpy.ndarray, color : List[int] = None) -> numpy.ndarray :
		if self.filter == 0 :
			image = color_balance(image = image, cr = 30, mg = -32, yb = 16)
			image = posterize(image = image, levels = 4)

		if self.filter == 1 :
			image = color_balance(image = image, cr = -36, mg = -37, yb = 39)
			image = posterize(image = image, levels = 4)

		if self.filter == 2 :
			image = posterize(image = image, levels = 2)

		if self.filter == 3 :
			image = color_balance(image = image, cr = 100, mg = -100, yb = -100)
			image = posterize(image = image, levels = 3)

		if self.filter == 4 :
			image = color_balance(image = image, cr = -100, mg = -100, yb = 100)
			image = posterize(image = image, levels = 3)

		if self.filter == 5 :
			image = color_balance(image = image, cr = -100, mg = 100, yb = -100)
			image = posterize(image = image, levels = 3)

		if self.filter == 6 :
			image = posterize(image = image, levels = 5)
			image = hue_saturation(image = image, v1 = -41, v2 = -15, v3 = 6)

		if self.filter == 7 :
			image = posterize(image = image, levels = 6)
			image = color_balance(image = image, cr = -29, mg = 40, yb = 100)

		if self.filter == 8 :
			image = hue_saturation(image = image, v1 = -41, v2 = -20, v3 = 25)
			image = posterize(image = image, levels = 4)

		if self.filter == 9 :
			image = color_balance(image = image, cr = 100, mg = -100, yb = -100)
			image = posterize(image = image, levels = 3)
			image = hue_saturation(image = image, v1 = -41, v2 = -10, v3 = 20)

		if self.filter == 10 :
			image = color_balance(image = image, cr = 34, mg = -38, yb = 24)
			image = posterize(image = image, levels = 4)
			image = color_balance(image = image, cr = -65, mg = 0, yb = 0)

		if self.filter == 11 :
			image = color_balance(image = image, cr = 40, mg = -40, yb = 28)
			image = posterize(image = image, levels = 4)
			image = color_balance(image = image, cr = -100, mg = -42, yb = 35)

		if self.filter == 12 :
			image = color_balance(image = image, cr = 45, mg = -45, yb = 35)
			image = posterize(image = image, levels = 4)

		if self.filter == 13 :
			image = color_balance(image = image, cr = 30, mg = -35, yb = 20)
			image = posterize(image = image, levels = 4)

		if self.filter == 14 :
			image = color_balance(image = image, cr = 30, mg = -32, yb = 16)
			image = posterize(image = image, levels = 4)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 15 :
			image = color_balance(image = image, cr = -36, mg = -37, yb = 39)
			image = posterize(image = image, levels = 4)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 16 :
			image = posterize(image = image, levels = 2)
			image = recoloring(image = image, color = color, location = (2, 2))

		if self.filter == 17 :
			image = color_balance(image = image, cr = 100, mg = -100, yb = -100)
			image = posterize(image = image, levels = 3)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 18 :
			image = color_balance(image = image, cr = -100, mg = -100, yb = 100)
			image = posterize(image = image, levels = 3)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 19 :
			image = color_balance(image = image, cr = -100, mg = 100, yb = -100)
			image = posterize(image = image, levels = 3)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 20 :
			image = posterize(image = image, levels = 5)
			image = hue_saturation(image = image, v1 = -41, v2 = -15, v3 = 6)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 21 :
			image = posterize(image = image, levels = 6)
			image = color_balance(image = image, cr = -29, mg = 40, yb = 100)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 22 :
			image = hue_saturation(image = image, v1 = -41, v2 = -20, v3 = 25)
			image = posterize(image = image, levels = 4)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 23 :
			image = color_balance(image = image, cr = 100, mg = -100, yb = -100)
			image = posterize(image = image, levels = 3)
			image = hue_saturation(image = image, v1 = -41, v2 = -10, v3 = 20)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 24 :
			image = color_balance(image = image, cr = 34, mg = -38, yb = 24)
			image = posterize(image = image, levels = 4)
			image = color_balance(image = image, cr = -65, mg = 0, yb = 0)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 25 :
			image = color_balance(image = image, cr = 40, mg = -40, yb = 28)
			image = posterize(image = image, levels = 4)
			image = color_balance(image = image, cr = -100, mg = -42, yb = 100)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 26 :
			image = color_balance(image = image, cr = 45, mg = -45, yb = 35)
			image = posterize(image = image, levels = 4)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 27 :
			image = color_balance(image = image, cr = 30, mg = -35, yb = 20)
			image = posterize(image = image, levels = 4)
			image = recoloring(image = image, color = color, location = None)

		if self.filter == 28 :
			image = posterize(image = image, levels = 2)
			image = recoloring(image = image, color = color, location = (3, 3))

		if self.filter == 29 :
			image = color_balance(image = image, cr = 30, mg = -35, yb = 20)
			image = posterize(image = image, levels = 4)
			image = recoloring(image = image, color = color, location = (3, 3))

		if self.filter == 30 :
			image = posterize(image = image, levels = 3)

		if self.filter == 31 :
			image = color_balance(image = image, cr = -100, mg = -100, yb = 100)
			image = posterize(image = image, levels = 3)
			image = recoloring(image = image, color = color, location = (4, 4))

		if self.filter == 32 :
			image = color_balance(image = image, cr = 30, mg = -40, yb = 16)
			image = posterize(image = image, levels = 3)

		if self.filter == 33 :
			image = color_balance(image = image, cr = 30, mg = -40, yb = 16)
			image = posterize(image = image, levels = 3)
			image = recoloring(image = image, color = color, location = None)

		return image
