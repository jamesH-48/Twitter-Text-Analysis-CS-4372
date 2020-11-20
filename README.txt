CS 4372 Assignment 5
James Hooper ~ NETID: jah171230
Hritik Panchasara ~ NETID: hhp160130
------------------------------------------------------------------------------------------------------------------------------------
- For this assignment we utilized PyCharm
- Python Version: 3.7
- Imported Packages:
	- os
	- re
	- time
	- nltk
	- tweepy
	- collections
KEY THINGS:
~ You may need to download the nltk packages 'punkt' and 'stopwords' for the code to run properly. These lines of code are commented out in the main function.

~ You need to also have the stanford-ner-4.0.0 folder in your directory where you are running the .py file.
~ YOU HAVE TO SET YOUR JAVA FILE PATH IF IT DOES NOT WORK PROPERLY
~ For one of our home PCs we had Java version jdk1.8.0_181.
~ This may need to be changed to run the stanford-ner package.
~ There is not other option but to do this on your own personal machine for the code to run properly.

~ The Twitter API keys will also be masked upon submission so you will need to use your own.
------------------------------------------------------------------------------------------------------------------------------------
FUNCTIONS & PARAMETERS
if __name__ == '__main__':
~ This function grabs the StanfordNERTagger, the interval_runtime (which is in seconds), and the num_of_intervals before calling the other two functions.
~ The function will call twitter_text to collect the tweets for their specific intervals.
~ Then the function will call word_counter for each interval to print out the final named entity count results.

def twitter_text(interval_runtime, num_of_intervals):
~ This function sets up the Twitter API listener and the query.
~ Will print the interval times and the tweets that come as they are streamed.
~ To set the query edit the QUERY part of the twitterStream.filter(track=[QUERY],is_async=True) line.

def word_counter(list_of_tweets, st, runtime):
~ Once the tweets are gathered for each interval this code will pre-process all the text taking out links, @'s, #'s, punctuation, and stopwords.
~ Once that is done the StanfordNERTagger will tag the words.
~ There are two counts being tracked for each interval: a collection of all the tokenized words and a collection of all the entity tagged words.
------------------------------------------------------------------------------------------------------------------------------------
- The Report has a quick explanation of how the tweets/data is exctracted and collected and the final analysis of the results.
~ The Log File has the results of the query analyzed in the report.