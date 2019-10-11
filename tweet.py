import tweepy
from datetime import datetime

#twitter authentication
f = open('keys.txt')
keys = f.read().split(',')
f.close()
CONSUMER_KEY = keys[0]
CONSUMER_SECRET =  keys[1]
ACCESS_KEY =  keys[2]
ACCESS_SECRET =  keys[3]
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def compose_tweet(data):
    last_week_spread = float(data["week"]["tenyr"]) - float(data["week"]["twoyr"])
    latest_spread = float(data["latest"]["tenyr"]) - float(data["latest"]["twoyr"])
    spread_diff = round((latest_spread - last_week_spread), 2)
    spread_change = ""
    if spread_diff > 0:
        spread_change = "up {:.2f}".format(spread_diff)
    elif spread_diff < 0:
        spread_change = "down {:.2f}".format(abs(spread_diff))
    else:
        spread_change = "no change"

    tweet = "As of {} at 5:00PM EST\n\nTwo Year Yield: {:.2f}\n\nTen Year Yield: {:.2f}\n\nSpread: {:.2f}, {} from last week ({:.2f})".format(data["latest"]["date"], float(data["latest"]["twoyr"]), float(data["latest"]["tenyr"]), latest_spread, spread_change, last_week_spread)

    '''
    if latest_spread >= 0:
        tweet = "As of {} at 5:00PM EST\n\nTwo Year Yield: {:.2f}\n\nTen Year Yield: {:.2f}\n\nSpread: {:.2f}, {} from last week ({:.2f})".format(data["latest"]["date"], float(data["latest"]["twoyr"]), float(data["latest"]["tenyr"]), latest_spread, spread_change, last_week_spread)
    else:
        tweet = "\U0001F6A8 \U0001F6A8 The 10-Year/2-Year Yield Curve Has Inverted \U0001F6A8 \U0001F6A8\n\nAs of {} at 5:00PM EST\n\nTwo Year Yield: {:.2f}\n\nTen Year Yield: {:.2f}\n\nSpread: {:.2f}, {} from last week ({:.2f})".format(data["latest"]["date"], float(data["latest"]["twoyr"]), float(data["latest"]["tenyr"]), latest_spread, spread_change, last_week_spread)
    '''
    
    return tweet

def send(data):
    tweet = compose_tweet(data)
    print(tweet)
	#post tweet
    #api.update_status(tweet)
    api.update_with_media("fig1.png", tweet)
	#log tweets
    timet = 'Tweeted at %s' % (datetime.now())
    print (timet)
