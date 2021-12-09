from library.methods_color import create_rgb565
from library.methods_color import create_rgba
from library.methods_color import hsv_2_rgb
from library.methods_color import rgb_2_hsv
from library.methods_color import rgb_value
from library.methods_color import rgb565_r
from library.methods_color import rgb565_g
from library.methods_color import rgb565_b
from library.methods_color import rgba_r
from library.methods_color import rgba_g
from library.methods_color import rgba_b
from library.methods_color import clamp_color_0_255
from library.methods_math import clamp

import random
import numpy
import math

#
#
#

def color_balance_init (red : int, green : int, blue : int, shadows : numpy.ndarray) -> list :
	def private_method (index : int, value : int) -> int :
		val = shadows[index] if value > 0 else shadows[255 - index]
		val = index + index * val

		return clamp_color_0_255(val)

	rlut = [private_method(index = index, value = red) for index in range(256)]
	glut = [private_method(index = index, value = green) for index in range(256)]
	blut = [private_method(index = index, value = blue) for index in range(256)]

	return rlut, glut, blut

#
# Applies the rgb565 filter to the given image
#

def color_balance_process_rgb565 (image : numpy.ndarray, rlut : list, glut : list, blut : list) -> numpy.ndarray :
	def private_method (element : int) -> int :
		r = rgb565_r(color = element)
		g = rgb565_g(color = element)
		b = rgb565_b(color = element)

		v = rgb_value(red = r, green = g, blue = b)

		r = rlut[r]
		g = glut[g]
		b = blut[b]

		h, s, _ = rgb_2_hsv(red = r, green = g, blue = b)
		r, g, b = hsv_2_rgb(hue = h, saturation = s, value = v)

		r = int(round(r))
		g = int(round(g))
		b = int(round(b))

		return create_rgb565(red = r, green = g, blue = b)

	return numpy.vectorize(private_method)(image)

#
# Applies the rgba filter to the given image
#

def color_balance_process_rgba (image : numpy.ndarray, rlut : list, glut : list, blut : list) -> numpy.ndarray :
	def private_method (element : int) -> int :
		r = rgba_r(color = element)
		g = rgba_g(color = element)
		b = rgba_b(color = element)

		v = rgb_value(red = r, green = g, blue = b)

		r = rlut[r]
		g = glut[g]
		b = blut[b]

		h, s, _ = rgb_2_hsv(red = r, green = g, blue = b)
		r, g, b = hsv_2_rgb(hue = h, saturation = s, value = v)

		r = int(round(r))
		g = int(round(g))
		b = int(round(b))

		return create_rgba(red = r, green = g, blue = b)

	return numpy.vectorize(private_method)(image)

#
#
#

def lut_init (levels : int) -> list :
	def private_method (index : int) -> float :
			value = index / 255.0
			value = int(round(value * (levels - 1.0)) / (levels - 1.0))
			value = 255.0 * value + 0.5

			return clamp_color_0_255(value)

	return [private_method(index = index) for index in range(256)]

#
# Applies the rgb565 filter to the given image
#

def lut_process_rgb565 (image : numpy.ndarray, lut : list) -> numpy.ndarray :
	def private_method (pixel : int) -> int :
		r = lut[rgb565_r(color = pixel)]
		g = lut[rgb565_g(color = pixel)]
		b = lut[rgb565_b(color = pixel)]

		r = int(round(r))
		g = int(round(g))
		b = int(round(b))

		return create_rgb565(red = r, green = g, blue = b)

	return numpy.vectorize(private_method)(image)

#
# Applies the rgba filter to the given image
#

def lut_process_rgb565 (image : numpy.ndarray, lut : list) -> numpy.ndarray :
	def private_method (pixel : int) -> int :
		r = lut[rgba_r(color = pixel)]
		g = lut[rgba_g(color = pixel)]
		b = lut[rgba_b(color = pixel)]

		r = int(round(r))
		g = int(round(g))
		b = int(round(b))

		return create_rgba(red = r, green = g, blue = b)

	return numpy.vectorize(private_method)(image)

#
#
#

def hue_saturation_init (hue : int, saturation : int, value : int) -> list :
	def compute_hue (index : int) -> float :
		color = hue * 255.0 / 360.0

		if index + color <   0 : return index + color + 255
		if index + color > 255 : return index + color - 255

		return index + color

	def compute_sat (index : int) -> float :
		color = saturation * 255.0 / 100.0
		color = clamp(color, -255, 255)

		return clamp_color_0_255(index * (255 + color) / 255)
	
	def compute_val (index : int) -> float :
		color = value * 127.0 / 100.0
		color = clamp(color, -255, 255)

		if color < 0 :
			return index * (255 + color) / 255

		return index + ((255 - index) * color) / 255

	lhue = [compute_hue(index = index) for index in range(256)]
	lsat = [compute_sat(index = index) for index in range(256)]
	lval = [compute_val(index = index) for index in range(256)]

	return lhue, lsat, lval

#
# Applies the rgb565 filter to the given image
#

def hue_saturation_process_rgb565  (image : numpy.ndarray, hue : list, saturation : list, value : list) -> numpy.ndarray :
	def private_method (pixel : int) -> int :
		r = rgb565_r(color = pixel)
		g = rgb565_g(color = pixel)
		b = rgb565_b(color = pixel)

		h, s, v = rgb_2_hsv(red = r, green = g, blue = b)

		h = hue[h]
		s = saturation[s]
		v = value[v]

		r, g, b = hsv_2_rgb(hue = h, saturation = s, value = v)

		return create_rgb565(red = r, green = g, blue = b)

	return numpy.vectorize(private_method)(image)

#
# Applies the rgba filter to the given image
#

def hue_saturation_process_rgba  (image : numpy.ndarray, hue : list, saturation : list, value : list) -> numpy.ndarray :
	def private_method (pixel : int) -> int :
		r = rgba_r(color = pixel)
		g = rgba_g(color = pixel)
		b = rgba_b(color = pixel)

		h, s, v = rgb_2_hsv(red = r, green = g, blue = b)

		h = hue[h]
		s = saturation[s]
		v = value[v]

		r, g, b = hsv_2_rgb(hue = h, saturation = s, value = v)

		return create_rgba(red = r, green = g, blue = b)

	return numpy.vectorize(private_method)(image)

#
# Applies the rgb565 recoloring to the image
#

def apply_rgb565_recoloring (image : numpy.ndarray, color : list = None, location : tuple = None) -> numpy.ndarray :
	if color is None :
		r = random.randrange(0, 256)
		g = random.randrange(0, 256)
		b = random.randrange(0, 256)
	else :
		r = clamp_color_0_255(color[0])
		g = clamp_color_0_255(color[1])
		b = clamp_color_0_255(color[2])

	if location is None :
		x = random.randrange(0, numpy.size(image, axis = 0))
		y = random.randrange(0, numpy.size(image, axis = 1))
	else :
		x = clamp(location[0], 0, numpy.size(image, axis = 0))
		y = clamp(location[1], 0, numpy.size(image, axis = 1))

	old_color = image[x, y]
	new_color = create_rgb565(red = r, green = g, blue = b)

	image[image == old_color] = new_color

	return image

#
# Applies the rgba recoloring to the image
#

def apply_rgba_recoloring (image : numpy.ndarray, color : list = None, location : tuple = None) -> numpy.ndarray :
	if color is None :
		r = random.randrange(0, 256)
		g = random.randrange(0, 256)
		b = random.randrange(0, 256)
	else :
		r = clamp_color_0_255(color[0])
		g = clamp_color_0_255(color[1])
		b = clamp_color_0_255(color[2])

	if location is None :
		x = random.randrange(0, numpy.size(image, axis = 0))
		y = random.randrange(0, numpy.size(image, axis = 1))
	else :
		x = clamp(location[0], 0, numpy.size(image, axis = 0))
		y = clamp(location[1], 0, numpy.size(image, axis = 1))

	old_color = image[x, y]
	new_color = create_rgba(red = r, green = g, blue = b)

	image[image == old_color] = new_color

	return image
