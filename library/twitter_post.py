from tweepy.models import Status
from tweepy import API

from datetime import datetime
from datetime import timezone

class TwitterPost :

	#
	# Create a twitter post object with a given status object
	#

	def __init__ (self, status : Status) -> None :
		self.status = status
		self.retweets = self.status.retweet_count
		self.likes = self.status.favorite_count
		self.id = self.status.id

		self.age = datetime.now(timezone.utc) - self.status.created_at
	#
	# Update the twitter information with the given api
	#

	def update_status (self, api : API) -> None :
		self.status = api.get_status(self.id)

		self.retweets = self.status.retweet_count
		self.likes = self.status.favorite_count

		self.age = datetime.now(timezone.utc) - self.status.created_at

	#
	# Returns true if this tweet has any retweets or likes, false otherwise
	#

	def activity (self) -> bool :
		return self.retweets > 0 or self.likes > 0

	#
	# Returns the number of retweets
	#

	def retweets (self) -> int :
		return self.retweets

	#
	# Returns the number of likes
	#

	def likes (self) -> int :
		return self.likes

	#
	# Returns the status of the tweet
	#

	def status (self) -> Status :
		return self.status

	#
	# Returns the age of the tweet in seconds
	#

	def age (self) -> int :
		return round(self.age.total_seconds())

	#
	# Returns the id of the tweet
	#

	def id (self) -> int :
		return self.id
