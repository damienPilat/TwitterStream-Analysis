"""
Using Botometer library to check the probability of a twitter account being ran by a bot.
Created by Damien Pilat.
"""

from botometer import Botometer     # Twitter bot checking library
from dotenv import load_dotenv      # Access .env files
import os                           # Open files from computer
import csv                          # Access .csv files

# load env file
load_dotenv()
# Print content based on verbose value. 0: Nothing, 1: Main elements, 2: everything
verbose = 1


# Check result of bot-score based on a threshold, and return the smallest difference if over
def checkBot(bot_score):
    bot_threshold = 0.65
    if bot_score['cap']['english'] > bot_threshold or bot_score['cap']['universal'] > bot_threshold:
        threshold_difference_one = bot_score['cap']['english'] - bot_threshold
        threshold_difference_two = bot_score['cap']['universal'] - bot_threshold
        smallest_margin = min([i for i in [threshold_difference_one, threshold_difference_two] if i > 0])
        if verbose != 0:
            print("Bot score above threshold by {}".format(smallest_margin))
        return smallest_margin
    return -1


# Store result of bot test in csv file
def storeBotResult(bot_score, usr_name):
    # Check if above threshold
    bot_margin = checkBot(bot_score)

    # Check file doesnt exist before creating file
    fileIndex = 0
    datafile = 'bot_check_'+str(fileIndex)+'.csv'
    while os.path.isfile(datafile):
        fileIndex += 1
        datafile = 'bot_check_' + str(fileIndex) + '.csv'

    # Open csv writer on file
    csvwriter = csv.writer(open(datafile, 'w'))
    csvwriter.writerow([usr_name, str(bot_margin)])


# Function to retrieve bot score, print elements and save results
def getBotScore(usr_name):
    bot_score = botometer.check_account('@'+usr_name)
    # Print english & universal scores
    if verbose == 2:
        print("english_score:", bot_score['cap']['english'], ", universal_score:", bot_score['cap']['universal'])

    # Print bot scores
    if verbose == 2:
        print(bot_score)

    # store bot result
    storeBotResult(bot_score, usr_name)


# Create object of Botometer w/ twitter keys
botometer = Botometer(rapidapi_key=os.getenv("RAPID_API_KEY"), consumer_key=os.getenv("CONSUMER_KEY"), consumer_secret=os.getenv("CONSUMER_SECRET"), wait_on_ratelimit=True)

# Open tweet_data file
csvreader = csv.reader(open('tweeters_ordered.csv', 'r'))
# Loop through 1st 480 elements
for idx, row in enumerate(csvreader):
    if idx == 0:
        getBotScore(row[0][1:])
    elif idx < 470:
        getBotScore(row[0])
