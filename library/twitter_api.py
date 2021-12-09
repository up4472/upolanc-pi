from library.twitter_post import TwitterPost

from tweepy import OAuthHandler
from tweepy import API

class TwitterAPI :

	#
	# Create a twitter api object with the given configuration and credentials dictionary
	#

	def __init__ (self, config : dict, credentials : dict) -> None :
		auth = OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
		auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])

		self.api = API(auth)

		self.enable = config['enable']
		self.caption = config['caption']
		self.tweets = []

		if self.enable :
			if config['verify'] :
				self.api.verify_credentials()

			for status in self.api.home_timeline(count = 60) :
				self.tweets.append(TwitterPost(status = status))

	#
	# Creates a new tweet with the media located at the specified filename and the given caption
	#

	def post_media (self, filename : str, caption : str = None) -> int :
		if not self.enable :
			return 0

		if caption is None :
			caption = self.caption

		status = self.api.update_status_with_media(caption, filename)
		tweet = TwitterPost(status = status)

		self.tweets.append(tweet)

		return tweet.get_id()

	#
	# Update the status of all the tweets
	#

	def update_status (self) -> None :
		if not self.enable :
			return

		map(lambda tweet : tweet.update_status(self.api), self.tweets)

	#
	# Delete tweets that are older than the specified time values
	#

	def delete_tweets (self, hours : int = 0, minutes : int = 0, seconds : int = 0) -> None :
		if not self.enable :
			return

		limit = 3600 * hours + 60 * minutes + seconds

		tweets = []

		for tweet in self.tweets :
			if not tweet.has_activity() :
				if tweet.get_age() > limit :
					self.api.destroy_status(id = tweet.get_id())
				else :
					tweets.append(tweet)

		self.tweets = tweets

	#
	# Returns true if the api is enabled, false otherwise
	#

	def is_enabled (self) -> bool :
		return self.enable
