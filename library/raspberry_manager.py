from library.raspberry_camera import RaspberryCamera
from library.raspberry_window import RaspberryWindow

from typing import Dict
from typing import Any

class RaspberryManager :

	#
	# Creates a new raspberry manager object
	#

	def __init__ (self) -> None :
		self.camera_manager = None
		self.window_manager = None

	#
	# Creates and returns a new raspberry camera manager
	#

	def init_camera (self, config : Dict[str, Any]) -> RaspberryCamera :
		self.camera_manager = RaspberryCamera(config = config)

		return self.camera_manager

	#
	# Creates and returns a new raspberry window manager
	#

	def init_window (self, config : Dict[str, Any]) -> RaspberryWindow :
		self.window_manager = RaspberryWindow(config = config)

		return self.window_manager

	#
	# Returns true if the close request has been created by the user, false otherwise
	#

	def close_requested (self) -> bool :
		return self.window_manager.close_requested()

	#
	# Stops and closes all processes
	#

	def stop (self) -> None :
		self.camera_manager.stop_preview()
		self.camera_manager.stop()
		self.window_manager.stop()
