import numpy
import cv2

#
# Load the image data
#

def load_image (filename : str, grayscale : bool = False) -> numpy.ndarray :
	image = cv2.imread(filename = filename)

	if grayscale :
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	return image
#
# Resize the image to the desired shape
#

def resize_image_to (image : numpy.ndarray, width : int, height : int) -> numpy.ndarray :
	return cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)

#
# Resize the image by the desired factor
#

def resize_image_by (image : numpy.ndarray, factor : float) -> numpy.ndarray :
	height = int(round(factor * numpy.size(image, axis = 0)))
	width = int(round(factor * numpy.size(image, axis = 1)))

	return resize_image_to(image = image, width = width, height = height)

#
# Save the image data
#

def save_image (filename : str, image : numpy.ndarray) -> None :
	cv2.imwrite(filename = filename, img = image)
