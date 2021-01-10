"""
Digital Sandbox : Cw2
Main file for retrieving tweets through Twitter Stream API.
Data is cleaned from special characters before being stored in csv files.
Created by Damien Pilat.
"""

import twitter          # Make use of Twitter API
import csv              # Write to csv files
import os               # make us of file access
from dotenv import load_dotenv  # make use of env files for password security

# Load env file
load_dotenv()

# Screen output buffer, 0: None, 1: Main tracking, 2: all
verbose = 1

# OAuth Authentication
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = os.getenv("OAUTH_TOKEN_SECRET")

# Twitter Authentication
auth = twitter.oauth.OAuth(
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
    CONSUMER_KEY, CONSUMER_SECRET,
)
# Connect to twitter API
twitter_api = twitter.Twitter(auth=auth)

# CSV file for data storage
fileIndex = 0
datafile = 'tweetStream_'+str(fileIndex)+'.csv'

# Check file doesnt exist, if so increment file number and retry
while os.path.isfile(datafile):
    fileIndex += 1
    datafile = 'tweetStream_'+str(fileIndex)

# Open csv writer on a new file
csvwriter = csv.writer(open(datafile, 'w'))

# Store all relevant data
tweet_data = {}


# Query terms
q = ['SpaceX', 'Elon Musk', 'Falcon', 'Starship', 'BocaChicaGal', 'Blue Origin', '#NewGlenn', 'Virgin Galactic', '#space', '#nasa', '#boeing', 'Erdayastronaut', 'commercial_crew', 'universe', 'astronomy', 'galaxy', 'moon', 'mars', '#astronaut', 'rocket', 'spaceship', 'milkyway', 'astrophysics', 'spaceexploration', 'outerspace', 'telescope', 'spacetravel', 'blackhole', 'moon', 'lunar', 'artemis', 'gateway', 'NasaKennedy', 'northropgrumman ', '@nasa_sls', 'nasa_orion', '@nasaortemis', 'launchAmerica']



# Resulting tweets from stream
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
stream = twitter_stream.statuses.filter(track="SpaceX")

# Data requested for storage
first_level_entries = ['geo', 'retweet_count', 'id', 'created_at', 'in_reply_to_user_id', 'text', 'truncated']
user_level_entries = ['screen_name', 'id', 'verified', 'statuses_count', 'friends_count', 'followers_count', 'favourites_count', 'location', 'description', 'created_at']


# Clean data of unrecognisable characters for analysis
def clean_data(data):
    clean = ""
    if data:
        if isinstance(data, int):
            return data
        data = data.replace('|', ' ')
        data = data.replace('\n', ' ')
        data = data.replace('\r', ' ')
        clean = data
    return clean


# Loop through stream output
for idx, tweet in enumerate(stream):
    if verbose != 0:
        print(tweet['id'])

    # Populate for first-level-entries
    for entry in first_level_entries:
        tweet_data[entry] = clean_data(tweet[entry])
    # Populate for user-level-entries
    for entry in user_level_entries:
        el_name = "usr_" + entry
        tweet_data[el_name] = clean_data(tweet['user'][entry])

    # Replace full text if truncated tweet
    if tweet['truncated']:
        tweet_data['text'] = clean_data(tweet['extended_tweet']['full_text'])

        if verbose != 0:
            print("truncated text found")
    if idx == 0:
        csvwriter.writerow([*tweet_data.keys()])
    csvwriter.writerow([*tweet_data.values()])
