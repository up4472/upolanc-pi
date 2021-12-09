from library.methods_cv import load_haar

import numpy

class FaceDetector :

	#
	# Creates a new face detector object with the given configuration dictionary
	#

	def __init__ (self, config : dict) -> None :
		self.name = config['model']
		self.detector = None

		if self.name == 'haar' :
			self.detector = load_haar(filename = config['haar_location'])
		if self.name == 'yolo5' :
			self.detector = None

	#
	# Runs the face detector algorithm on the given image
	#

	def detect_face (self, image : numpy.ndarray) -> list :
		bbox = []

		if self.name == 'haar' :
			bbox = self.detector.detectMultiScale(image, scaleFactor = 1.3, minNeighbors = 3)
		if self.name == 'yolo5' :
			...

		return bbox
