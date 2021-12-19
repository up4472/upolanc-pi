from typing import Tuple

import math

#
# Compute the euclidian distance between the centers of two bounding boxes (x, y, w, h)
#

def compute_distance (src : Tuple[int, int, int, int], dst : Tuple[int, int, int, int]) -> float :
	x1 = src[0] + 0.5 * src[2]
	y1 = src[1] + 0.5 * src[3]
	x2 = dst[0] + 0.5 * dst[2]
	y2 = dst[1] + 0.5 * dst[3]

	return math.hypot(x2 - x1, y2 - y1)

#
# Clamp value between 0 and 255
#

def clamp0255 (value : float) -> float :
	return clamp(value = value, minval = 0, maxval = 255)

#
# Clamp value between the given range
#

def clamp (value : float, minval : float, maxval : float) -> float :
	return max(min(value, maxval), minval)
