from library.methods_math import compute_distance
from library.methods_math import clamp

from typing import List
from typing import Dict
from typing import Any

import random
import numpy

class FaceSelector :

	#
	# Creates a new face detector object with the given configuration dictionary
	#

	def __init__ (self, config : Dict[str, Any]) -> None :
		self.distance = config['bbox_distance']
		self.method = config['method']
		self.factor = config['bbox_resize']
		self.location = None

	#
	# Select a bounding box based on the method type defined in the initialization
	#

	def select_bbox (self, bounding_box : List[int]) -> list :
		if len(bounding_box) == 1 :
			return numpy.array(bounding_box[0]).flatten()

		if len(bounding_box) > 1 :
			if self.method == 'random' or self.location is None :
				index = random.randrange(len(bounding_box))

				return numpy.array(bounding_box[index]).flatten()

			if self.method == 'distance_max' :
				distances = [compute_distance(self.location, bbox) for bbox in bounding_box]

				index = distances.index(max(distances))

				return numpy.array(bounding_box[index]).flatten()

			if self.method == 'distance_weighted' :
				distances = [compute_distance(self.location, bbox) for bbox in bounding_box]
				distances = [distance if distance > self.distance else 1e-5 for distance in distances]

				cumulative = sum(distances)

				probability = [distance / cumulative for distance in distances]
				population = numpy.arange(len(bounding_box))

				index = random.choices(population = population, weights = probability)

				return numpy.array(bounding_box[index]).flatten()

		return []

	#
	# Crop the bounding box from the image
	#

	def crop_image (self, image : numpy.ndarray, bounding_box : List[int]) -> numpy.ndarray :
		x = bounding_box[0] - 0.5 * (self.factor - 1) * bounding_box[2]
		y = bounding_box[1] - 0.5 * (self.factor - 1) * bounding_box[3]
		w = bounding_box[2] * self.factor
		h = bounding_box[3] * self.factor

		img_w = numpy.size(image, axis = 0)
		img_h = numpy.size(image, axis = 1)

		x = clamp(x, 0, img_w)
		y = clamp(y, 0, img_h)
		w = clamp(w, 0, img_w)
		h = clamp(h, 0, img_h)

		x = int(round(x))
		y = int(round(y))
		w = int(round(w))
		h = int(round(h))

		if numpy.ndim(image) == 3 :
			return image[y:y + h, x:x + w, :]

		return image[y:y + h, x:x + w]

	#
	# Update the last used bounding box
	#

	def update_location (self, bounding_box : List[int]) -> None :
		self.location = bounding_box
