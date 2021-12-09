from picamera import PiCamera

class RaspberryCamera :

	#
	# Creates a new raspberry camera object with the given configuration dictionary
	#

	def __init__ (self, config : dict) -> None :
		self.width = config['width']
		self.height = config['height']

		self.camera = PiCamera(
			resolution = (self.width, self.height),
			framerate = config['framerate']
		)

		self.camera.iso = config['iso']
		self.camera.rotation = config['rotation']

		self.preview_enable = config['preview']['enable']
		self.preview_fullscreen = config['preview']['fullscreen']

		self.preview_location = [
			config['preview']['x'],
			config['preview']['y'],
			config['preview']['width'],
			config['preview']['height']
		]

	#
	# Capture the image from the picamera and save it to the given filename
	#

	def capture (self, filename : str) -> None :
		self.camera.capture(filename)

	#
	# Starts and opens the picamera object preview
	#

	def start_preview (self) -> None :
		if self.preview_enable :
			self.camera.start_preview(fullscreen = self.preview_fullscreen, window = self.preview_location)

	#
	# Stops and closes the picamera object preview
	#

	def stop_preview (self) -> None :
		self.camera.stop_preview()

	#
	# Stops and closes the picamera object
	#

	def stop (self) -> None :
		self.camera.close()
