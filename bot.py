import time
import tweepy
import crawler
import threading
from secrets import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)


mentionTweetsList = []
repliedTweetsList = [996903445440294913, 996651221288079360, 996559374402256896]

def filterCommand(tweet):
	"""
	Call the adequated function according to the command requested in the current tweet
	"""
	tweetText = tweet.text.split(" ")
	newsArticle = ''
	message = ''

	#check which command was called by the user and perform its corresponding action and return it
	if tweetText[1] == "!noticias":
		articles = crawler.getRequestedNews(tweetText[2])
		#append the header, description and link to the resulting message
		for article in articles['articles']:
			newsArticle += ('{} \n'.format(article['source']['name']))
			newsArticle += ('{} \n'.format(article['description']))
			newsArticle += ('{} \n'.format(article['url']))
			message += (newsArticle)
			message += '\n'
		return (message, tweet.id)
	elif tweetText[1] == '!creador':
		return ('Mi creador es Daniel Gaytan | @dnigaytan', tweet.id)
	else:
		return ('Unknown command: {}'.format(tweetText[1]), tweet.id)

def tweetMessage(message, replyID = None):
	"""
	Receive the message as a parameter and tweet it 
	"""
	remainingCharacters = 260
	tweet = ''

	if remainingCharacters - len(message) >= 0:
		api.update_status(message, in_reply_to_status_id = replyID)
	else:
		#divide el mensaje recibido en fragmentos por cada salto de linea
		message = message.split('\n')
		for fragment in message:
			#check if the whole fragment can be placed within the tweet without exceed the characters limit
			if remainingCharacters - len(fragment) >= 0:
				tweet += fragment
				remainingCharacters -= len(fragment)
			else:
				if replyID:
					lastTweet = api.update_status(tweet, in_reply_to_status_id = replyID)
					replyID = lastTweet.id
					print('funciona')
				else:
					api.update_status(tweet)
					print('funciona ')
				#reset the characters limit because the tweet has been sent
				remainingCharacters = 280
				#reset the tweet text with the new value fragment, because the actual fragment was discarded in order to send
				#the tweet without exceeding the limit size
				tweet = fragment

def checkNewMentions():
	"""
	Check for new mentions using the search function, all the new mentions will be saved
	in the mentionTweetsList list 
	"""
	#check if mentionTweetsList has no mentions inside it
	if len(mentionTweetsList) == 0:
		newMentions = api.mentions_timeline()

		for mention in newMentions:
			#check if the current mention tweet has been replied by the bot by comparing
			#its id with the repliedTweetsList ids 
			if mention.id not in repliedTweetsList:
				mentionTweetsList.append(mention)

def deleteOldMentions():
	"""
	Delete the mentions that had been replied by the bot and have a date older than a week
	"""
	pass

def replyTweet():
	"""
	Reply to each mention tweet
	"""
	for tweet in mentionTweetsList:
		resultMessage, replyID = filterCommand(tweet)
		tweetMessage(resultMessage, replyID)
		repliedTweetsList.append(tweet.id)





#checkNewMentions()
#replyTweet()
#print(repliedTweetsList)

checkingMentions = threading.Thread(target='runInfiniteLoop', args = 'checkNewMentions')
replyingTweets = threading.Thread(target='runInfiniteLoop', args = 'replyTweet()')
checkingMentions.start()





		









                             