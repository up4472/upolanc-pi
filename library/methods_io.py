from typing import Dict
from typing import Any

import json
import os

#
# Returns true if the file exists, false otherwise
#

def file_exists (filename : str) -> bool :
	return os.path.exists(filename)

#
# Deletes the file if it exists
#

def file_delete (filename : str) -> None :
	if file_exists(filename = filename) :
		os.remove(filename)

#
# Load a json file into a dictionary object
#

def load_json (filename : str) -> Dict[str, Any] :
	if file_exists(filename = filename) :
		with open(filename, 'r') as file :
			return json.load(file)

#
# Create a directory if the directory does not exist
#

def dir_create (directory : str) -> None :
	if not file_exists(filename = directory) :
		os.mkdir(directory)

#
# Deletes the directory if it exists
#

def dir_delete (directory : str) -> None :
	if file_exists(filename = directory) :
		os.rmdir(directory)
