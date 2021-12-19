from library.methods_color import rgb_to_hls
from library.methods_color import hls_to_rgb
from library.methods_color import rgb_to_l
from library.methods_math import clamp0255
from library.methods_math import clamp

from typing import Tuple
from typing import List

import random
import numpy
import cv2

def f1 (i : int) -> float :
	return 0.667 * (1 - ((float(i) - 127.0) / 127.0) ** 2)

def f2 (i : int) -> float :
	return 1.075 - 1 / (float(i) / 16.0 + 1)

SHADOW_ADD = numpy.array([f1(i) for i in range(256)], dtype = float)
SHADOW_SUB = numpy.array([f2(i) for i in range(255, -1, -1)], dtype = float)

def color_balance (image : numpy.ndarray, cr : int, mg : int, yb : int) -> numpy.ndarray :
	global SHADOW_ADD
	global SHADOW_SUB

	crt = numpy.array([SHADOW_ADD[i] if cr > 0 else SHADOW_SUB[255 - i] for i in range(256)], dtype = float)
	mgt = numpy.array([SHADOW_ADD[i] if mg > 0 else SHADOW_SUB[255 - i] for i in range(256)], dtype = float)
	ybt = numpy.array([SHADOW_ADD[i] if yb > 0 else SHADOW_SUB[255 - i] for i in range(256)], dtype = float)

	rlut = numpy.array([clamp0255(i + cr * crt[i]) for i in range(256)], dtype = numpy.uint8)
	glut = numpy.array([clamp0255(i + mg * mgt[i]) for i in range(256)], dtype = numpy.uint8)
	blut = numpy.array([clamp0255(i + yb * ybt[i]) for i in range(256)], dtype = numpy.uint8)

	width = numpy.size(image, axis = 1)
	height = numpy.size(image, axis = 0)

	for hi in range(height) :
		for wi in range(width) :
			r = image[hi, wi, 2]
			g = image[hi, wi, 1]
			b = image[hi, wi, 0]

			r_n = rlut[r]
			g_n = glut[g]
			b_n = blut[b]

			r_n, g_n, b_n = rgb_to_hls(r_n, g_n, b_n)
			g_n = rgb_to_l(r, g, b)
			r_n, g_n, b_n = hls_to_rgb(r_n, g_n, b_n)

			image[hi, wi, 2] = r_n
			image[hi, wi, 1] = g_n
			image[hi, wi, 0] = b_n

	return image.astype(numpy.uint8)

def hue_saturation (image : numpy.ndarray, v1 : int, v2 : int, v3 : int) -> numpy.ndarray :
	def f1 (i : int, value : float) -> float :
		if i + value < 0 : return 255 + i + value
		if i + value > 255 : return i + value - 255

		return i + value

	def f2 (i : int, value : float) -> int :
		value = clamp(value, -255, 255)

		if value < 0 : value = (i * (255 + value)) / 255
		else : value = (i + ((255 - i) * value) / 255)

		return int(value)

	def f3 (i : int, value : float) -> float :
		value = clamp(value, -255, 255)
		value = clamp0255((i * (255 + value)) / 255)

		return value

	htl = numpy.array([f1(i, v1 * 255.0 / 360.0) for i in range(256)], dtype = float)
	ltl = numpy.array([f2(i, v2 * 127.0 / 100.0) for i in range(256)], dtype = numpy.uint8)
	stl = numpy.array([f3(i, v3 * 255.0 / 360.0) for i in range(256)], dtype = float)

	width = numpy.size(image, axis = 1)
	height = numpy.size(image, axis = 0)

	for hi in range(height) :
		for wi in range(width) :
			r = image[hi, wi, 2]
			g = image[hi, wi, 1]
			b = image[hi, wi, 0]

			h, l, s = rgb_to_hls(r, g, b)

			h = htl[int(h)]
			l = ltl[int(l)]
			s = stl[int(s)]

			r, g, b = hls_to_rgb(h, l, s)

			image[hi, wi, 2] = r
			image[hi, wi, 1] = g
			image[hi, wi, 0] = b

	return image.astype(numpy.uint8)

def posterize (image : numpy.ndarray, levels : int) -> numpy.ndarray :
	x = numpy.arange(256)

	ibins = numpy.linspace(0, 255, levels + 1)
	obins = numpy.linspace(0, 255, levels)

	label = numpy.digitize(x, ibins) - 1
	label[255] = levels - 1

	y = numpy.array(obins[label], dtype = int)

	image = cv2.LUT(image, y, image)

	return image.astype(numpy.uint8)

def recoloring (image : numpy.ndarray, color : List[int] = None, location : Tuple[int, int] = None) -> numpy.ndarray :
	if color is None :
		r = random.randrange(0, 256)
		g = random.randrange(0, 256)
		b = random.randrange(0, 256)
	else :
		r = clamp0255(color[0])
		g = clamp0255(color[1])
		b = clamp0255(color[2])

	if location is None :
		x = random.randrange(0, numpy.size(image, axis = 1))
		y = random.randrange(0, numpy.size(image, axis = 0))
	else :
		x = clamp(location[0], 0, numpy.size(image, axis = 1))
		y = clamp(location[1], 0, numpy.size(image, axis = 0))

	width = numpy.size(image, axis = 1)
	height = numpy.size(image, axis = 0)

	for hi in range(height) :
		for wi in range(width) :
			if image[hi, wi, 0] != image[x, y, 0] :
				continue
			if image[hi, wi, 1] != image[x, y, 1] :
				continue
			if image[hi, wi, 2] != image[x, y, 2] :
				continue

			image[hi, wi, 2] = r
			image[hi, wi, 1] = g
			image[hi, wi, 0] = b

	return image.astype(numpy.uint8)
