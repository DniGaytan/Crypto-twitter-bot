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
	messageList = []

	#check which command was called by the user and perform its corresponding action and return it
	if tweetText[1] == "!noticias":
		articles = crawler.getRequestedNews(tweetText[2])
		#append the header, description and link to the resulting message
		for article in articles['articles']:
			#for testing purposes
			print(article)
			messageList.append(article['url'])

		return (messageList, tweet.id, True)

	elif tweetText[1] == '!creador':
		return ('Mi creador es Daniel Gaytan | @dnigaytan', tweet.id, False)
	else:
		return ('Unknown command: {}'.format(tweetText[1]), tweet.id, False)

def tweetMessage(message, replyID, isList = False, screenName = None):
	"""
	Receive the message as a parameter and tweet it 
	"""
	remainingCharacters = 260
	tweetMessage = ''

	#if the message is a list '[...]' it will trigger the isList if statement, for everything else, it will pass
	#directly to the else statement
	if isList:
		#for each element in the message list, send it as a tweet separately
		for element in message:
			api.update_status('@{} {}'.format(screenName,element), in_reply_to_status_id = replyID)
	else:
		if remainingCharacters - len(message) >= 0:
			api.update_status(message, in_reply_to_status_id = replyID)
		else:
			#divide el mensaje recibido en fragmentos por cada espacio
			message = message.split(' ')

			for fragment in message:

				#check if the fragment can be placed within the tweet without exceeding the characters limit
				if remainingCharacters - (len(fragment) + 1)  >= 0:
					tweet += fragment + ' '
					remainingCharacters -= (len(fragment) + 1)
				else:
					if replyID is not None:
						lastTweet = api.update_status(tweet, in_reply_to_status_id = replyID)
						replyID = lastTweet.id
						print('funciona con reply')
					else:
						api.update_status(tweet)
						print('funciona ')
					#reset the characters limit because the tweet has been sent
					remainingCharacters = 260 - (len(fragment) + 1)	
					#reset the tweet text with the new value fragment, because the actual fragment was discarded in order to send
					#the tweet without exceeding the limit size
					tweet = fragment + ' '

	

def checkNewMentions():
	"""
	Check for new mentions using the search function, all the new mentions will be saved
	in the mentionTweetsList list 
	"""
	#check if mentionTweetsList has no mentions inside it
	if len(mentionTweetsList) <= 0:
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
		resultMessage, replyID, isList = filterCommand(tweet)
		tweetMessage(resultMessage, tweet.id, isList, screenName = tweet.user.screen_name)
		print('tweet contestado')
		repliedTweetsList.append(tweet.id)
		mentionTweetsList.remove(tweet)

def loadRepliedTweetsFile():
	repliedTweetsFile = open('repliedTweetsIDs.txt', 'r+')
	pass



def filterKeywords():
	pass




if __name__ == '__main__':
	while True:
		checkNewMentions()
		print(repliedTweetsList)
		replyTweet()
		time.sleep(20)




		









                             