from typing import Tuple
from typing import List
from typing import Dict
from typing import Any

import pygame
import qrcode
import numpy
import copy

class RaspberryWindow :

	#
	# Creates a new raspberry window object with the given configuration dictionary
	#

	def __init__ (self, config : Dict[str, Any]) -> None :
		pygame.init()
		pygame.font.init()

		if config['fullscreen'] :
			self.window = pygame.display.set_mode((config['width'], config['height']), pygame.FULLSCREEN)
		else :
			self.window = pygame.display.set_mode((config['width'], config['height']))

		self.mode = config['mode']
		self.font = pygame.font.SysFont(config['font-family'], config['font-size'])

		pygame.display.set_caption(config['title'])

	#
	# Fills the window with black color
	#

	def clean (self, color : Tuple[int, int, int] = None) -> None :
		if color is None :
			color = (0, 0, 0)

		self.window.fill(color)

	#
	# Render the images in a grid type format (1x1, 1x2, 2x2, 2x4)
	#

	def render_images (self, images : List[numpy.ndarray]) -> None :
		def process_mode (images : List[numpy.ndarray]) :
			if self.mode == 0 :
				w, h = self.resolution()

				if w >= 2 * h :
					self.mode = 2
				else :
					self.mode = 1

			if self.mode == 1 :
				images = [pygame.surfarray.make_surface(image) for image in images]
				images = [pygame.transform.rotate(image, -90) for image in images]

				return images

			mirrored = [copy.deepcopy(image) for image in images]
			mirrored = [pygame.surfarray.make_surface(image) for image in mirrored]
			mirrored = [pygame.transform.rotate(image, -90) for image in mirrored]
			mirrored = [pygame.transform.flip(image, True, False) for image in mirrored]

			images = [pygame.surfarray.make_surface(image) for image in images]
			images = [pygame.transform.rotate(image, -90) for image in images]

			return images + mirrored

		def process_images (images : List[pygame.Surface], win_w : int, win_h : int) :
			if len(images) == 2 :
				win_w = win_w / 2

			elif len(images) == 4 :
				win_w = win_w / 2
				win_h = win_h / 2

			elif len(images) == 8 :
				win_w = win_w / 4
				win_h = win_h / 2

			img_w = images[0].get_width()
			img_h = images[0].get_height()

			scale = min(win_w / img_w, win_h / img_h)
			scale = 0.90 * scale

			img_w = int(img_w * scale)
			img_h = int(img_h * scale)

			loc_x = int(0.5 * (win_w - img_w))
			loc_y = int(0.5 * (win_h - img_h))

			images = [pygame.transform.scale(image, (img_w, img_h)) for image in images]
			locations = numpy.zeros(shape = (len(images), 2), dtype = int)

			pad_w = 0.5 * (win_w - img_w)
			pad_h = 0.5 * (win_h - img_h)

			padding = min(pad_w, pad_h)

			pad_w = pad_w - padding
			pad_h = pad_h - padding

			if len(images) == 1 :
				locations[0] = [loc_x, loc_y]

			elif len(images) == 2 :
				locations[0] = [loc_x        , loc_y]
				locations[1] = [loc_x + win_w, loc_y]

			elif len(images) == 4 :
				locations[0] = [loc_x + pad_w        , loc_y + pad_h]
				locations[1] = [loc_x - pad_w + win_w, loc_y + pad_h]

				locations[2] = [loc_x + pad_w        , loc_y - pad_h + win_h]
				locations[3] = [loc_x - pad_w + win_w, loc_y - pad_h + win_h]

			elif len(images) == 8 :
				locations[0] = [loc_x +     pad_w        , loc_y + pad_h]
				locations[1] = [loc_x + 2 * pad_w + win_w, loc_y + pad_h]
				locations[2] = [loc_x +     pad_w        , loc_y - pad_h + win_h]
				locations[3] = [loc_x + 2 * pad_w + win_w, loc_y - pad_h + win_h]

				locations[5] = [loc_x -     pad_w + 2 * win_w, loc_y + pad_h]
				locations[4] = [loc_x - 2 * pad_w + 3 * win_w, loc_y + pad_h]
				locations[7] = [loc_x -     pad_w + 2 * win_w, loc_y - pad_h + win_h]
				locations[6] = [loc_x - 2 * pad_w + 3 * win_w, loc_y - pad_h + win_h]

			return images, locations

		win_w, win_h = self.resolution()

		images = process_mode(images = images)
		images, locations = process_images(images = images, win_w = win_w, win_h = win_h)

		for image, location in zip(images, locations) :
			self.window.blit(image, location)

	def render_qrcode (self, text : str, location : Tuple[int, int]) -> None :
		qr = qrcode.QRCode(version = 1, box_size = 2, border = 1)
		qr.add_data(text)
		qr.make(fit = True)

		qr.make_image(fill = 'black', back_color = 'white').save('qrcode.png')

		image = pygame.image.load('qrcode.png')

		win_w, win_h = self.resolution()
		loc_w, loc_h = location

		image_w = image.get_width()
		image_h = image.get_height()

		w = max(0, min(loc_w, win_w - image_w - 1))
		h = max(0, min(loc_h, win_h - image_h - 1))

		self.window.blit(image, (w, h))

	#
	# Render the counter
	#

	def render_text (self, text : str, location : Tuple[int, int], color : Tuple[int, int, int] = None) -> None :
		if color is None : color = (255, 255, 255)

		text = self.font.render(text, False, color)

		win_w, win_h = self.resolution()
		loc_w, loc_h = location

		text_w = text.get_width()
		text_h = text.get_height()

		w = max(0, min(loc_w, win_w - text_w - 1))
		h = max(0, min(loc_h, win_h - text_h - 1))

		self.window.blit(text, (w, h))

	#
	# Updates the pygame window by flipping the buffer
	#

	def update (self) -> None :
		pygame.display.flip()

	#
	# Stops and closes the pygame window
	#

	def stop (self) -> None :
		pygame.quit()

	#
	# Returns true if the close request has been created by the user, false otherwise
	#

	def close_requested (self) -> bool :
		state = pygame.key.get_pressed()

		if state[pygame.K_ESCAPE] :
			return True

		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				return True

		return False

	#
	# Returns the resolution of the pygame window
	#

	def resolution (self) -> list :
		return self.window.get_size()
