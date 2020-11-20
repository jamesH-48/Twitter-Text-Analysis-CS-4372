import os
import re
import time
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from collections import Counter

# Word/Entity Counter
def word_counter(list_of_tweets, st, runtime):
	#print("List of Tweets:")
	index = 0
	all_words = []
	only_tagged_words = []
	for tweet in list_of_tweets:
		index+=1
		#print("Tweet #", index, ": ")

		# Gets rid of links
		text = re.sub(r'http\S+', '', tweet)
		# Gets rid of @'s (@POTUS, @user2424, etc.)
		text = re.sub(r'@\S+', '', text)
		# Gets rid of #'s (#WTF, #BREAKING, etc.)
		text = re.sub(r'#\S+', '', text)
		# Gets rid of punctuation
		text = re.sub(r'[^\w\s]', '', text)
		# Change to lower-case to not have repeats (the, The, THE, etc.)
		# text = text.lower()
		# Remove stop words
		stop_words = set(stopwords.words('english'))
		tokenized_text = word_tokenize(text)
		filtered_sentence = []
		for w in tokenized_text:
			if w not in stop_words:
				filtered_sentence.append(w)

		all_words.extend(filtered_sentence)
		classified_text = st.tag(filtered_sentence)
		for text in classified_text:
			if text[1] != 'O':
				only_tagged_words.append((text[0],text[1]))
		#print(classified_text)

	# Final Print
	print("=======================================================================")
	print("Runtime: ", runtime, "seconds")
	print("Count of All Words: ")
	counted_words = Counter(all_words)
	for key, value in counted_words.items():
		print(key, value)
	print()
	print("Count of All Entity Tagged Words: ")
	counted_ent_words = Counter(only_tagged_words)
	for key, value in counted_ent_words.items():
		print(key, value)

def twitter_text(interval_runtime, num_of_intervals):
	#consumer key, consumer secret, access token, access secret.
	ckey="sdfsddsf"
	csecret="sdfdsdsf"
	atoken="sdfs-sdfsd"
	asecret="sdfsfds"

	# Maintains the entire set of tweets over all intervals
	list_of_tweets = []
	# Example intervals
	# [0] 0 - 5 seconds
	# [1] 0 - 10 seconds
	# [2] 0 - 15 seconds
	# [3] 0 - 20 seconds
	# [4] 0 - 25 seconds
	# Should always have 5 appended
	# List of list_of_tweets for different intervals
	# Basically keeps adding new tweets as intervals progress
	# (Tw1, Tw2), (Tw1, Tw2, Tw3), (Tw1, Tw2, Tw3, Tw4, Tw5), etc...
	interval_tweets = []

	# Listener class for tweepy connection with Twitter API
	class listener(StreamListener):
		def on_status(self, status):
			# Gets rid of retweets
			# If not a retweet and attempt to check this status an error will occur
			# So we need the try, except to catch the error
			try:
				if status.retweeted_status:
					return
			except:
				pass
			if status.lang != 'en':
				return
			print("--------------------------------------------------------------")
			print(status.text)
			print("--------------------------------------------------------------")
			# print(status.user.screen_name)
			list_of_tweets.append(status.text)

		def on_error(self, status):
			print(status)

	# Set keys
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)

	# Connect to stream with selected filter
	twitterStream = Stream(auth, listener(), tweet_mode= 'extended')
	# Must be async for disconnection to work properly
	twitterStream.filter(track=["NASA", "SpaceX", "Crew1", "Crew-1"],is_async=True)

	# Print current time
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	print("========")
	print(current_time)
	print("========")

	for i in range(num_of_intervals):
		# Sleep for interval_runtime duration to be connected for that time
		time.sleep(interval_runtime)
		# Grab this intervals list of tweets
		interval_tweets.append(list_of_tweets[:])
		# Print current time
		t = time.localtime()
		current_time = time.strftime("%H:%M:%S", t)
		print("========")
		print(current_time)
		print("========")

	# disconnect the stream and stop streaming
	twitterStream.disconnect()

	return interval_tweets

if __name__ == '__main__':
	# Use this to download punkt package
	# import nltk as nltk
	# nltk.download('punkt')
	# nltk.download('stopwords')

	# YOU HAVE TO SET YOUR JAVA FILE PATH IF IT DOES NOT WORK PROPERLY
	java_path = "C:/Program Files/Java/jdk1.8.0_181/bin/java.exe"
	os.environ['JAVAHOME'] = java_path
	cwd = os.getcwd()
	st = StanfordNERTagger(cwd + '\stanford-ner-4.0.0\classifiers\english.muc.7class.distsim.crf.ser.gz',
						   cwd + '\stanford-ner-4.0.0\stanford-ner.jar',
						   encoding='utf-8')

	# Set the runtime for the connection to run for
	# There will always be 5 intervals
	# interval_runtime = 5 == 5 seconds
	# if interval_runtime = 5 seconds && num_of_intervals = 5
	# -> total_runtime = 25 seconds
	interval_runtime = 12
	num_of_intervals = 5

	print("Interval Runtime: ", interval_runtime)
	print("Number of Intervals: ", num_of_intervals)

	# Call main api function call to gather tweets/text
	interval_tweets = twitter_text(interval_runtime, num_of_intervals)


	# Call to pre-process and count entities with StandfordNERtagger
	# We do this for each interval of time
	runtime = 0
	for list_of_tweets in interval_tweets:
		runtime += interval_runtime
		word_counter(list_of_tweets, st, runtime)