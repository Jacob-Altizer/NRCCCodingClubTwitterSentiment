##Main file for the Twitter Sentiment analysis project for the NRCC Coding Club
##Authors: Aidan Murphy

##Import Resources
import re
from time import sleep
import tweepy
from tweepy import OAuthHandler
import textblob
from dotenv import load_dotenv
import os
import pytwits as pt
import streamlit as st

load_dotenv()

##Authorize Twitter Clients via class
class twitterclient(object):
    
    def __init__(self):
    
        self.auth = tweepy.OAuth2BearerHandler(os.environ.get('Bearer_token'))
        self.api = tweepy.API(self.auth)

    ## first func, Clean tweets of hyperlinks
    def clean_tweet(self, tweet):
    
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    ## Second func, Analyze tweets for sentiment
    def get_tweet_sentiment(self, tweet):

        ## Use textblob to analyze sentiment
        analysis = textblob.TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    ## third func, get retweet count
    def get_retweet_count(self, tweet):
        
        count = self.api.get_status(tweet)
        return count

    ## fourth func, get last tweet of user
    def get_last_tweet(self,account):
        
        tweets = []
        
        tweet = self.api.user_timeline(id=account, count = 1, tweet_mode = "extended")[0]
        
        tweets.append(tweet)

        for tweet in tweets:

                parsed_tweet = {}
                parsed_tweet['text'] = tweet.full_text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text)
                parsed_tweet['retweet_count'] = tweet.retweet_count

                print("Date: " + str(tweet.created_at))
                print("Text: "+str(parsed_tweet['text']) + "\n")
                print("Sentiment: "+str(parsed_tweet['sentiment']))
                print("Retweets: "+str(parsed_tweet['retweet_count']))
                print("Likes: " + str(tweet.favorite_count))



    ## fifth func, retrieve tweets
    def get_tweets(self, query, count=3000):
        
        ## create tweet list
        tweets = []

        ## get tweets containing phrase
        try:
            fetched_tweets = self.api.search_tweets(q=query, count = count, tweet_mode = 'extended')
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.full_text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text)
                parsed_tweet['retweet_count'] = tweet.retweet_count
                parsed_tweet['user'] = tweet.user
                parsed_tweet['screen_name'] = tweet.user.screen_name
                parsed_tweet['profile_pic'] = tweet.user.profile_image_url
                parsed_tweet['num_likes'] = tweet.favorite_count
                
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepyException as e:
            print("ERROR: " + str(e))

## Get tweets then add them to positive or negative tweets based on sentiment
def main():
    
    ## Oauth
    api = twitterclient()

    st.write("-------------------------------------------------------")
    tweets = api.get_tweets(query = user_input, count = Tweets_to_analyze)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    st.text("Positive tweets percentage:\t {} %".format(100*len(ptweets)/len(tweets)))
    st.text("Negative tweets percentage:\t {} %".format(100*len(ntweets)/len(tweets)))
    st.text("Neutral tweets percentage: \t {} %".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))
    st.text("-------------------------------------------------------")


# if __name__ == "__main__":
#     main()
