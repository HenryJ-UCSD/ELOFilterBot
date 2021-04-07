#!/usr/bin/python3

# Import libraries
import time
import praw
import requests
from bs4 import BeautifulSoup

# Reddit login API
reddit = praw.Reddit(
	client_id='d8oBBP_J6Gm6pg',
	client_secret='Bw5YiRaUQmVvk3n5quxzYNXdrwo',
	username='Showdown_ModBot',
	password='',
	user_agent='Showdown_ModBot by /u/SimonThePug',
	)

# Which subreddits to listen on
subreddits = reddit.subreddit('pokemonshowdown')

while True:
	for submission in subreddits.stream.submissions(skip_existing=True):
		if ('replay.pokemonshowdown.com' in submission.url):
			urlString = submission.url

			# The web page to scrape
			page = requests.get(urlString)

			# Create a BeautifulSoup object
			soup = BeautifulSoup(page.text, 'html.parser')

			# Pull the information from the small text tag
			small_text = soup.find('small',{'class':'uploaddate'}).text

			if ('Rating' in small_text):
				# Split the information into two strings (before and after 'Rating: ')
				splitstring = (small_text.split('Rating: ',1))

				# Store the second string
				rank_text = splitstring.pop(1)
				if (submission.title.startswith(rank_text, 1)):
					pass
				else:
					submission.mod.remove()
					autoReply = submission.reply('''
Hello!

It looks like the ELO rating attached to your replay does not match the number you've submitted, or you've forgotten to include the ELO tag in your title.

For reference, the correct ELO is ''' + rank_text + '''. Please enclose it in square brackets at the start of your post like this [''' + rank_text + '''].

Your post has been automatically removed. If you would like to resubmit, please verify the ELO in your title is correct.

If you believe your post was removed in error, please message the moderators of this subreddit.
					'''
					)
					autoReply.mod.distinguish(sticky=True)
			elif ('Rating' not in small_text and submission.title.startswith('[', 0)):
				pass
			elif ('Rating' not in small_text and submission.title.startswith('(', 0)):
				pass
			else:
				submission.mod.remove()
				autoReply = submission.reply('''
Hello!

It looks like you have forgotten to include an ELO tag. Please revisit the replay and give your best estimate as to the ELO.

The ELO will be the loser of the replay's ranking after the match. Enclose it in square brackets at the beginning of your post like this: [1234]

Your post has been automatically removed. If you would like to resubmit, please verify the ELO in your title is correct.

If you believe your post was removed in error, please message the moderators of this subreddit.
					'''
				)
				autoReply.mod.distinguish(sticky=True)
		else:
			pass
