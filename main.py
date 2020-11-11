import os
import re
import time
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# Use this to download punkt package
#import nltk as nltk
#nltk.download('punkt')

# YOU HAVE TO SET YOUR JAVA FILE PATH IF IT DOES NOT WORK PROPERLY
java_path = "C:/Program Files/Java/jdk1.8.0_181/bin/java.exe"
os.environ['JAVAHOME'] = java_path

cwd = os.getcwd()
st = StanfordNERTagger(cwd + '\stanford-ner-4.0.0\classifiers\english.muc.7class.distsim.crf.ser.gz',
					   cwd + '\stanford-ner-4.0.0\stanford-ner.jar',
					   encoding='utf-8')

text = 'On Sunday that playing time went to rookie defensive end Neville Gallimore, and if his performance was any indication then his future looks a lot brighter than the Cowboys\' present.'

tokenized_text = word_tokenize(text)
classified_text = st.tag(tokenized_text)

print(classified_text)

#consumer key, consumer secret, access token, access secret.
ckey="sdgsdgg"
csecret="sdgsgsdg"
atoken="sdgsd"
asecret="sdgdgsdg"


list_of_tweets = []

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
		print(status.text)
		print(status.user.screen_name)
		list_of_tweets.append(status.text)
	def on_error(self, status):
		print(status)

# Set keys
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

# Get current time
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)

# Set the runtime for the connection to run for
runtime = 15

# Connect to stream with selected filter
twitterStream = Stream(auth, listener(), tweet_mode= 'extended')
# Must be async for disconnection to work properly
twitterStream.filter(track=["#COVID19"],is_async=True)

# Sleep for runtime duration to be connected for that time
time.sleep(runtime)
# disconnect the stream and stop streaming
twitterStream.disconnect()

# Get current time
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)

print("List of Tweets:")
index = 0
for tweet in list_of_tweets:
	index+=1
	print("Tweet #", index, ": ")
	print(type(tweet))
	# Gets rid of links
	text = re.sub(r'http\S+', '', tweet)
	# Gets rid of @'s (@POTUS, @user2424, etc.)
	text = re.sub(r'@\S+', '', text)
	# Gets rid of #'s (#WTF, #BREAKING, etc.)
	text = re.sub(r'#\S+', '', text)
	print(text)
	tokenized_text = word_tokenize(text)
	classified_text = st.tag(tokenized_text)
	print(classified_text)
