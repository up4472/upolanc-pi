import numpy

#
# Clamp color value between 0 and 255
#

def clamp_color_0_255 (value : int) -> int :
	return max(min(value, 255), 0)

#
# Create RGBA color
#

def create_rgba (red : int, green : int, blue : int, alpha : int = 255) -> int :
	return alpha << 24 | blue << 16 | green << 8 | red

#
# Get red component from RGBA color
#

def rgba_r (color : int) -> int :
	return (color & 0x000000FF)

#
# Get green component from RGBA color
#

def rgba_g (color : int) -> int :
	return (color & 0x0000FF00) >> 8

#
# Get blue component from RGBA color
#

def rgba_b (color : int) -> int :
	return (color & 0x00FF0000) >> 16

#
# Get alpha component from RGBA color
#

def rgba_a (color : int) -> int :
	return (color & 0xFF000000) >> 24

#
# Create RGB565 color
#

def create_rgb565 (red : int, green : int, blue : int) -> int :
	return (red >> 3) << 11 | (green >> 2) << 5 | blue >> 3

#
# Get red component from RGB565 color
#

def rgb565_r (color : int) -> int :
	 return ((color & 0xF800) >> 11) << 3

#
# Get green component from RGB565 color
#

def rgb565_g (color : int) -> int :
	return ((color & 0x07E0) >> 5) << 2

#
# Get blue component from RGB565 color
#

def rgb565_b (color : int) -> int :
	return (color & 0x001F) << 3

#
# Transform RGB to HSV format
#

def rgb_2_hsv (red : int, green : int, blue : int) -> list :
	maxcolor = max(red, green, blue)
	mincolor = min(red, green, blue)

	hue = 0.0
	sat = 0.0
	val = 0.5 * (maxcolor + mincolor)

	if maxcolor != mincolor :
		cdif = float(maxcolor - mincolor)
		csum = float(maxcolor + mincolor)

		if val < 128 :
			sat = 255 * cdif / csum
		else :
			sat = 255 * cdif / (511.0 - csum)

		if red == maxcolor :
			hue = (green - blue) / cdif

		elif green == maxcolor :
			hue = 2 + (blue - red) / cdif

		else :
			hue = 4 + (red - green) / cdif

		hue = 42.5 * hue

		if hue > 255 : hue = hue - 255
		if hue <   0 : hue = hue + 255

	hue = int(round(hue))
	sat = int(round(sat))
	val = int(round(val))

	return hue, sat, val

#
# Transform HSV to RGB format
#

def hsv_2_rgb (hue : int, saturation : int, value : int) -> list :
	r = value
	g = value
	b = value

	if saturation != 0 :
		if value < 128 :
			m2 = (value * (255 + saturation)) / 65025.0
		else :
			m2 = (value + saturation - (value * saturation) / 255.0) / 255.0

		m1 = (value / 127.5) - m2

		r = hsv_value(m1, m2, hue + 85)
		g = hsv_value(m1, m2, hue)
		b = hsv_value(m1, m2, hue - 85)

	r = int(round(r))
	g = int(round(g))
	b = int(round(b))

	return r, g, b

#
# Get the average value of the min and max components
#

def rgb_value (red : int, green : int, blue : int) -> int :
	maxcolor = max(red, green, blue)
	mincolor = min(red, green, blue)

	return 0.5 * (maxcolor + mincolor)

#
# Get the average value of the components
#

def hsv_value (x : float, y : float, hue : float) -> int :
	if hue > 255 : hue = hue - 255
	if hue <   0 : hue = hue + 255

	if hue < 42.5 :
		value = x + (y - x) * (hue / 42.5)

	elif hue < 127.5 :
		value = y

	elif hue < 170 :
		value = x + (y - x) * ((170 - hue) / 42.5)

	else :
		value = x

	return int(255 * value)

#
# Transform cv's RGB to RGB565 format
#

def transform_cv2_rgb565 (image : numpy.ndarray) -> numpy.ndarray :
	img_h = numpy.size(image, axis = 0)
	img_w = numpy.size(image, axis = 1)

	image_rgb = numpy.zeros((img_h, img_w), dtype = int)

	for row in range(img_h) :
		for col in range(img_w) :
			r = image[row, col, 0]
			g = image[row, col, 1]
			b = image[row, col, 2]

			image_rgb[row, col] = create_rgb565(red = r, green = g, blue = b)

	return image_rgb

#
# Transform cv's RGB to RGBA format
#

def transform_cv2_rgba (image : numpy.ndarray) -> numpy.ndarray :
	img_h = numpy.size(image, axis = 0)
	img_w = numpy.size(image, axis = 1)

	image_rgb = numpy.zeros((img_h, img_w), dtype = int)

	for row in range(img_h) :
		for col in range(img_w) :
			r = image[row, col, 0]
			g = image[row, col, 1]
			b = image[row, col, 2]

			image_rgb[row, col] = create_rgba(red = r, green = g, blue = b)

	return image_rgb

#
# Transform RGB565 to cv's RGB format
#

def transform_rgb565_cv2 (image : numpy.ndarray) -> numpy.ndarray :
	img_h = numpy.size(image, axis = 0)
	img_w = numpy.size(image, axis = 1)

	image_cv2 = numpy.zeros((img_h, img_w, 3), dtype = int)

	for row in range(img_h) :
		for col in range(img_w) :
			image_cv2[row, col, 0] = rgb565_r(color = image[row, col])
			image_cv2[row, col, 1] = rgb565_g(color = image[row, col])
			image_cv2[row, col, 2] = rgb565_b(color = image[row, col])

	return image_cv2

#
# Transform RGBA to cv's RGB format
#

def transform_rgba_cv2 (image : numpy.ndarray) -> numpy.ndarray :
	img_h = numpy.size(image, axis = 0)
	img_w = numpy.size(image, axis = 1)

	image_cv2 = numpy.zeros((img_h, img_w, 3), dtype = int)

	for row in range(img_h) :
		for col in range(img_w) :
			image_cv2[row, col, 0] = rgba_r(color = image[row, col])
			image_cv2[row, col, 1] = rgba_g(color = image[row, col])
			image_cv2[row, col, 2] = rgba_b(color = image[row, col])

	return image_cv2
