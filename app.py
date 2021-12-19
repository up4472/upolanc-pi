import os

from library.methods_io import dir_delete, file_delete

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os.environ['SDL_VIDEO_CENTERED'] = '1'

from threading import Timer
from threading import Thread

from library import FilterManager
from library import FaceDetector
from library import FaceSelector
from library import RaspberryManager
from library import TwitterAPI

from library import destroy_all_windows
from library import display_bbox
from library import resize_image_by
from library import resize_image_to
from library import load_image
from library import save_image

from library import __version__
from library import __author__

import traceback
import datetime
import random
import numpy
import time
import json

# Location constants
TMP_DIR = 'tmp'

if not os.path.exists(TMP_DIR) :
	os.mkdir(TMP_DIR)

FILE_CAPTURE	= os.path.join(TMP_DIR, 'capture.png')
FILE_FACE		= os.path.join(TMP_DIR, 'profile.png')
FILE_FILTER		= os.path.join(TMP_DIR, 'filters.png')

#
# Load configuration and twitter credentials
#

with open('configuration.json', 'r') as file :
	config = json.load(file)

with open('credentials.json', 'r') as file :
	credentials = json.load(file)

#
# Debug flag
#

DEBUG = config['debug']

#
# Set up values if debug mode is on
#

if DEBUG :
	# Lock random
	random.seed(63130192)

	# Set testing image for debug mode
	FILE_CAPTURE = 'profile.png'

	# Enable camera preview
	config['camera']['preview']['enable'] = True
	config['camera']['preview']['fullscreen'] = False

	# Window information for camera preview
	config['camera']['preview']['x'] = 1425
	config['camera']['preview']['y'] = 25
	config['camera']['preview']['width'] = 400
	config['camera']['preview']['height'] = 400

	# Window information
	config['window']["width"] = 640
	config['window']['height'] = 480
	config['window']['fullscreen'] = False

	# Window information for displaying bounding boxes
	config['detector']['preview']['x'] = 25
	config['detector']['preview']['y'] = 25
	config['detector']['preview']['width'] = 400
	config['detector']['preview']['height'] = 400

	# Method for filter selection
	config['filter']['method'] = 'iterative'

	# Disable twitter api
	config['api']['enable'] = False
	config['api']['qrcode'] = True

#
# Define time constants
#

COUNTDOWN_TIMER = config['countdown']

CAPTURE_START_FRAME = config['run_capture']
FILTERS_START_FRAME = config['run_filters']

CAPTURE_START_FRAME = max(min(CAPTURE_START_FRAME, COUNTDOWN_TIMER), 0)
FILTERS_START_FRAME = max(min(FILTERS_START_FRAME, COUNTDOWN_TIMER), 0)

if CAPTURE_START_FRAME == 0 :
	CAPTURE_START_FRAME = COUNTDOWN_TIMER

if FILTERS_START_FRAME == 0 :
	FILTERS_START_FRAME = COUNTDOWN_TIMER

#
# Initailize raspberry manager and its devices
#

app_manager = RaspberryManager()

app_camera = app_manager.init_camera(config = config['camera'])
app_window = app_manager.init_window(config = config['window'])

app_detector = FaceDetector(config = config['detector'])
app_selector = FaceSelector(config = config['selector'])

app_twitter = TwitterAPI(config = config['api'], credentials = credentials)

app_filter = FilterManager(config = config['filter'])

#
# Display bounding box location
#

bbox_location = [
	config['detector']['preview']['x'],
	config['detector']['preview']['y'],
	config['detector']['preview']['width'],
	config['detector']['preview']['height']
]

#
# The last frame data
#

last_capture = None
last_filter = []
last_face = None
last_id = 'N/A'

#
# The running flag
#

running = False

#
# The capture + detection thread method
#

def detect_face () :
	# print(f'Thread : {datetime.datetime.now()} : capture + detection')

	# Set global variables
	global app_detector
	global app_selector
	global app_camera
	global last_capture
	global last_face
	global running

	# Check close requesed
	if not running :
		return

	# Capture the image
	if not DEBUG :
		app_camera.capture(filename = FILE_CAPTURE)

	# Load the captured image
	image = load_image(filename = FILE_CAPTURE)

	# Downscale the captured image
	size = max(numpy.shape(image))

	if size > 512 :
		image = resize_image_by(image = image, factor = 512 / size)

	# Detect faces from the loaded image
	bbox = app_detector.detect_face(image = image)

	# Print detection information
	print(f'Thread : {datetime.datetime.now()} : capture + detection -> {len(bbox)} face(s) detected')

	if len(bbox) > 0 :
		# Select a single face based on selected algorithm
		bbox = app_selector.select_bbox(bounding_box = bbox)

		# Crop the image based on the bounding box plus padding
		last_face = app_selector.crop_image(image = image, bounding_box = bbox)

		# Update the last used bounding box
		app_selector.update_location(bounding_box = bbox)

		# Resize the image to a uniform size
		last_face = resize_image_to(image = last_face, width = 128, height = 128)

#
# The filter thread method
#

def apply_filters () :
	print(f'Thread : {datetime.datetime.now()} : filter')

	# Set global variables
	global running
	global app_filter
	global app_twitter
	global last_filter
	global last_face
	global last_id

	# Check close requesed
	if not running or last_face is None :
		return

	# Aplly the filter to the image in RGB565 format
	last_filter = app_filter.apply_filters(image = last_face, color = None)

	# Save the first image
	save_image(filename = FILE_FILTER, image = last_filter[0])

	# Create a twitter post
	last_id = app_twitter.post_media(filename = FILE_FILTER, caption = None)

#
# The twitter update thread method
#

def twitter_update (hours : int = 0, minutes : int = 0, seconds : int = 0) :
	# Set global variables
	global app_twitter
	global running

	if app_twitter.is_enabled() :
		print(f'Thread : {datetime.datetime.now()} : twitter -> api enabled')
	else :
		print(f'Thread : {datetime.datetime.now()} : twitter -> api disabled')

	# Check close requesed
	if not running :
		return

	# Update the twitter post information
	app_twitter.update_status()

	# Delete twitter posts without any activity over the time limit
	app_twitter.delete_tweets(hours = hours, minutes = minutes, seconds = seconds)

	# Run the thread again after 15 seconds
	Timer(interval = 15.0, function = twitter_update, args = [hours, minutes, seconds]).start()

#
# The main render thread method
#

def main () :
	# Set global variables
	global app_manager
	global app_window
	global app_camera
	global running
	global last_filter
	global last_face
	global last_id

	# Load last face if it exists
	if os.path.exists(FILE_FACE) :
		last_face = load_image(filename = FILE_FACE)

	# Start the application
	timer = COUNTDOWN_TIMER
	running = True

	# Start all the threads
	twitter_update(minutes = 5)

	# Calculate border positions
	win_w, win_h = app_window.resolution()

	BL = (    0, win_h)
	BR = (win_w, win_h)

	# First detector + filter run
	detect_face()
	apply_filters()

	try :
		# Check close requesed
		while running :
			print(f'Thread : {datetime.datetime.now()} : main')

			# Check close requested
			running = not app_manager.close_requested()

			if not running :
				print()
				print('INFO : Closing application by user request')
				print('INFO : Waiting for other threads')

				break

			# Clean the window
			app_window.clean()

			# Render the captured image to the screen
			if len(last_filter) > 0 :
				app_window.render_images(images = last_filter)

			# Set strings
			timer_str = str(timer).rjust(2, '0')
			qcode_str = str(last_id)
	
			# Render timer
			app_window.render_text(text = timer_str, location = BL)

			# Render last tweet id
			if config['api']['qrcode'] :
				app_window.render_qrcode(text = qcode_str, location = BR)
			else :
				app_window.render_text(text = qcode_str, location = BR)

			# Update the window to display the image
			app_window.update()

			# Update timer
			timer = timer - 1

			if timer <= 0 :
				timer = COUNTDOWN_TIMER
				print()

			# Run filters on the start of the time frame
			if timer == FILTERS_START_FRAME :
				Thread(target = apply_filters, daemon = True).start()

			# Run detection a few seconds beforehand
			if timer == CAPTURE_START_FRAME :
				Thread(target = detect_face, daemon = True).start()

			# Sleep for 1 second
			time.sleep(1.0)

	# Catch user keyboard interrupt
	except KeyboardInterrupt :
		print()
		print('INFO : User keyboard interrupt caught')
		print('INFO : Waiting for other threads')

	# Catch other excpetions
	except Exception :
		print()
		print('ERROR : Uncaught exception has occured')
		print('INFO : Waiting for other threads')

		traceback.print_exc()

	running = False

	# Destroy all hanging cv2 windows
	# FIXME when DEBUG is true display_bbox seem to prevent from exiting the application
	destroy_all_windows()

	# Delete temporary files
	if not DEBUG :
		file_delete(FILE_CAPTURE)

	file_delete(FILE_FILTER)
	file_delete(FILE_FACE)
	dir_delete(TMP_DIR)

	# Stop any devices running
	app_manager.stop()

#
# Entry point
#

if __name__ == '__main__' :
	print(f'Version : {__version__}')
	print(f'Author  : {__author__}')
	print()

	main()
