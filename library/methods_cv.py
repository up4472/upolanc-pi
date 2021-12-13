import numpy
import copy
import time
import cv2
import os

#
# Create and load the haar cascade classifier
#

def load_haar (filename : str) -> cv2.CascadeClassifier :
	filename = os.path.join(cv2.data.haarcascades, filename)

	return cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, filename))

#
# Display the bouding boxes of the detected faces on the given image
#

def display_bbox (image : numpy.ndarray, bounding_box : list, location : list) -> None :
	xloc = location[0]
	yloc = location[1]
	wloc = location[2]
	hloc = location[3]

	image = copy.deepcopy(image)

	for x, y, w, h in bounding_box :
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

	winname = f'Number of detected faces : {len(bounding_box)}'

	cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
	cv2.moveWindow(winname, xloc, yloc)
	cv2.imshow(winname, image)
	cv2.resizeWindow(winname, wloc, hloc)

	cv2.waitKey(1)

	cv2.destroyWindow(winname)

#
# Destroy all cv2 windows
#

def destroy_all_windows () -> None :
	cv2.destroyAllWindows()
